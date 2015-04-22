#!/bin/sh

DOMAIN='brasil.gov.agenda'

# List of languages
LANGUAGES="en pt_BR"

# Assume I18NDUDE is installed with buildout
# and this script is run under src/ folder with three nested namespaces in the package name
I18NDUDE=../../../../bin/i18ndude

if test ! -e $I18NDUDE; then
        I18NDUDE=i18ndude
        if test ! -e $I18NDUDE; then
                echo "No i18ndude was found in buildout or in your \$PATH."
                exit 1
        fi
fi

 # Create locales folder structure for languages
install -d locales
for lang in $LANGUAGES; do
    install -d locales/$lang/LC_MESSAGES
done

# Do we need to merge manual PO entries from a file called manual.pot.
# this option is later passed to i18ndude
#
if test -e locales/${DOMAIN}-manual.pot; then
        echo "Manual PO entries detected"
        MERGE="--merge locales/${DOMAIN}-manual.pot"
else
        echo "No manual PO entries detected"
        MERGE=""
fi

$I18NDUDE rebuild-pot --pot ./locales/${DOMAIN}.pot $MERGE --create ${DOMAIN} .  || exit 1
$I18NDUDE sync --pot ./locales/${DOMAIN}.pot ./locales/*/LC_MESSAGES/${DOMAIN}.po

$I18NDUDE rebuild-pot --pot ./locales/plone.pot --create plone ./profiles/default  || exit 1
$I18NDUDE sync --pot ./locales/plone.pot ./locales/*/LC_MESSAGES/plone.po

WARNINGS=`find . -name "*pt" | xargs $I18NDUDE find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs $I18NDUDE find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs $I18NDUDE find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs $I18NDUDE find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./locales/rebuild_i18n.log
touch ./locales/rebuild_i18n.log

find ./ -name "*pt" | xargs $I18NDUDE find-untranslated > ./locales/rebuild_i18n.log
