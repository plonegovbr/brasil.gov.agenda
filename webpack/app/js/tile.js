import DatePicker from './datepicker.js';


export default class AgendaTile {
  constructor(tile) {
    this.tile = tile;
    this.datepicker = new DatePicker(this.tile, this.onDateChange.bind(this));
  }
  onDateChange(result) {
    debugger;
  }
}
