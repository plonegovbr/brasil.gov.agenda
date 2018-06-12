import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container, this.onDateChange.bind(this), true);
    this.$appointments = this.$('.list-compromissos');
    this.tzname = container.dataset.tzname;
  }
  $(selector) {
    return $(selector, this.container.parentElement);
  }
  extractTime(dateTime) {
    let [, time] = dateTime.split('T');
    let [hours, minutes, ] = time.split(':');
    return `${zfill(hours)}h${zfill(minutes)}`;
  }
  onDateChange(agendaDiaria) {
    this.$appointments.html('');
    if (typeof agendaDiaria.items === 'undefined') {
      this.$appointments.append(`
        <li class="sem-compromisso item-compromisso">
          <span>Atualmente não existem compromissos agendados.</span>
        </li>
      `);
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
      let $item = $(`
        <li class="item-compromisso-wrapper">
          <div class="item-compromisso">
            <div class="compromisso-horarios">
              <time class="horario compromisso-inicio"
                    datetime="${compromisso.start_date}">
                ${this.extractTime(compromisso.start_date)}
              </time>
            </div>
            <div class="compromisso-dados">
              <h4 class="compromisso-titulo">${compromisso.title}</h4>` +
              (compromisso.location == null? '' : `<p class="compromisso-local">${compromisso.location}</p>`) +
              `<span class="download-compromisso">
                <a class="add-agenda vcal" href="${compromisso['@id']}/vcal_view">VCAL</a>
                <span>Adicionar ao meu calendário</span>
              </span>
            </div>
          </div>
        </li>
      `);
      let now = new Date();
      let start_date = new Date(`${compromisso.start_date}${this.tzname}:00`);
      let end_date = new Date(`${compromisso.end_date}${this.tzname}:00`);
      // Javascript getTime method return timestamp
      if (now.getTime() > start_date.getTime() && now.getTime() < end_date.getTime()) {
        $('.compromisso-horarios', $item).append('<div class="now">Agora</div>')
      }
      this.$appointments.append($item);
    }
  }
}
