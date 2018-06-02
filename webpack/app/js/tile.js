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
  onDateChange(agendaDiaria) {
    this.swiper.removeAllSlides();
    this._$slide = $('<div class="swiper-slide"></div>');
    if (typeof agendaDiaria.items === 'undefined') {
      this._$slide.addClass('no-events');
      this._$slide.html('Sem compromissos oficiais.');
      this.swiper.appendSlide(this._$slide);
      return;
    }
    this.compromissos = [];
    for (let item of agendaDiaria.items) {
      $.ajax({
        headers: {
          Accept: 'application/json'
        },
        url: item['@id'],
        global: false,
        async: false,
        context: this,
      }).done((compromisso) => {
        this.compromissos.push(compromisso);
      });
    }
    this.compromissos.sort((a, b) => {
      return new Date(a.start_date) - new Date(b.start_date);
    });
    for (let compromisso of this.compromissos) {
      if (this._$slide.children().length === this.pageSize) {
        this.swiper.appendSlide(this._$slide);
        this._$slide = $('<div class="swiper-slide"></div>');
      }
      let now = new Date();
      let start_date = new Date(compromisso.start_date);
      let end_date = new Date(compromisso.end_date);
      let $item = $(`
        <div class="collection-events-item">
          <a class="title-item" href="${compromisso['@id']}">${compromisso.title}</a>
          <div class="location-item">
            <span class="location">${compromisso.location}</span>
          </div>
          <div class="timestamp-cell">
            <span class="timestamp">
              ${zfill(start_date.getHours())}h${zfill(start_date.getMinutes())}
            </span>
          </div>
        </div>
      `);
      if (now.getTime() > start_date.getTime() && now.getTime() < end_date.getTime()) {
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
