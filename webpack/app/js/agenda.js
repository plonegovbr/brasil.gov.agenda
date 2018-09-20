import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container);
    this.$appointments = this.$('.list-compromissos');
    this.editable = container.dataset.editable === 'True';
    if (this.editable) {
      this.makeOverlayEdit();
    }
  }
  $(selector) {
    return $(selector, this.container.parentElement);
  }
  makeOverlayEdit(){
    for (let item of $('.item-compromisso-wrapper')) {
      $('.editar_compromisso', item).prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: '#form',
        cssclass: 'overlay-compromisso',
        noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
        redirect: location.href,
        closeselector: '[name="form.buttons.cancel"]',
        width:'50%'
      });
      $('.remover_compromisso', item).prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: '#delete_confirmation',
        cssclass: 'overlay-compromisso',
        noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
        redirect: location.href,
        closeselector: '[name="form.button.Cancel"]',
        width:'50%'
      });
    }
  }
}
