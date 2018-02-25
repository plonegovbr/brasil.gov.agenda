import DatePicker from './datepicker.js';


export default class AgendaTile {
  constructor(tile) {
    this.tile = tile;
    new DatePicker(this.tile);
  }
}
