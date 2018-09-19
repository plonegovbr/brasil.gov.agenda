import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container);
    this.$appointments = this.$('.list-compromissos');
    this.editable = container.dataset.editable === 'True';
  }
  $(selector) {
    return $(selector, this.container.parentElement);
  }
}
