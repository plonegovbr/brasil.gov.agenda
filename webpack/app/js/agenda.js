import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container);
    this.$appointments = this.$('.list-compromissos');
    this.bindEvents();
  }
  $(selector) {
    return $(selector, this.container.parentElement);
  }
  bindEvents(){
    this.$('.editar_compromisso').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#form',
      cssclass: 'overlay-compromisso',
      noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
      redirect: location.href,
      closeselector: '[name="form.buttons.cancel"]',
      width:'50%'
    });
    this.$('.remover_compromisso').prepOverlay({
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
