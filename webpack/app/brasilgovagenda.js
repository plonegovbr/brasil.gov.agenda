// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];

class DatePicker {
  constructor(tile) {
    this.$tile = $(tile);
    this.$month = this.$('.monthpicker .month');
    this.$year = this.$('.monthpicker .year');
    this.$monthPickerInput = this.$('.monthpicker input');
    this.initMonthPicker();
  }
  $(selector) {
    return $(selector, this.$tile);
  }
  update() {
    this.updateMonthPicker();
  }
  updateMonthPicker() {
    let monthNamesShort = this.$monthPickerInput.datepicker('option', 'monthNamesShort');
    this.$month.html(monthNamesShort[this.month].toUpperCase());
    this.$year.html(this.year);
    $('.monthpicker').attr('data-month', this.month);
    $('.monthpicker').attr('data-year', this.year);
  }
  initMonthPicker() {
    this.$monthPickerInput.datepicker( {
      changeMonth: true,
      changeYear: true,
      showButtonPanel: true,
      onChangeMonthYear: (month, year, inst) => {
        $('#ui-datepicker-div').addClass('ui-selected');
      },
      onClose: function(dateText, inst) { 
        if (!$('#ui-datepicker-div').hasClass('ui-selected')) {
          return;
        }
        $('#ui-datepicker-div').removeClass('ui-selected');
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.$monthPickerInput.datepicker('setDate', new Date(this.year, this.month, 1));
        this.update();
      }.bind(this),
      beforeShow: (input, inst) => {
        $('#ui-datepicker-div').addClass('ui-monthpicker');
      }
    });
  }
}

$(() => {
  for (let agenda of $('.agenda-tile')) {
    new DatePicker(agenda);
  }
});

export default {
  DatePicker,
};
