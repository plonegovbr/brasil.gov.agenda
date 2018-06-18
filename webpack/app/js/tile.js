import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaTile {
  constructor(tile) {
    this.tile = tile;
    this.pageSize = 3;
    this.datepicker = new DatePicker(this.tile, this.onDateChange.bind(this));
    this.initSwiper();
    this.$('.is-now').append('<div class="now">Agora</div>')
  }
  $(selector) {
    return $(selector, this.tile);
  }
  extractTime(dateTime) {
    let [, time] = dateTime.split('T');
    let [hours, minutes, ] = time.split(':');
    return `${zfill(hours)}h${zfill(minutes)}`;
  }
  onDateChange(agendaDiaria) {
    this.swiper.removeAllSlides();
    this._$slide = $('<div class="swiper-slide"></div>');
    if (agendaDiaria.hasAppointments === false) {
      this._$slide.addClass('no-events');
      this._$slide.html('Sem compromissos oficiais.');
      this.swiper.appendSlide(this._$slide);
      return;
    }
    for (let compromisso of agendaDiaria.items) {
      if (this._$slide.children().length === this.pageSize) {
        this.swiper.appendSlide(this._$slide);
        this._$slide = $('<div class="swiper-slide"></div>');
      }
      let $item = $(`
        <div class="collection-events-item">
          <a class="title-item" href="${compromisso.href}">${compromisso.title}</a>` +
          (compromisso.location == null? '' : `<div class="location-item">
            <span class="location">${compromisso.location}</span>
          </div>`) +
          `<div class="timestamp-cell">
            <span class="timestamp">
              ${compromisso.start}
            </span>
          </div>
        </div>
      `);
      if (compromisso.isNow) {
        $('.timestamp-cell', $item).addClass('is-now');
        $('.timestamp-cell', $item).append('<div class="now">Agora</div>')
      }
      this._$slide.append($item);
    }
    if (this._$slide.children().length > 0) {
      this.swiper.appendSlide(this._$slide);
    }
  }
  initSwiper() {
    this.swiper = new Swiper(`#${this.tile.id} .collection-events`, {
      navigation: {
        nextEl: `#${this.tile.id} .collection-events .swiper-button-next`,
        prevEl: `#${this.tile.id} .collection-events .swiper-button-prev`,
      },
      pagination: {
        el: `#${this.tile.id} .collection-events .swiper-pagination`,
        clickable: true,
      },
    });
  }
}
