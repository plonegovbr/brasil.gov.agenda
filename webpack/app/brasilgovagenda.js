import AgendaTile from './js/tile.js';
import AgendaView from './js/agenda.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
  for (let tile of $('.agenda-tile')) {
    new AgendaTile(tile);
  }
  for (let container of $('.dados-agenda')) {
    new AgendaView(container);
  }
});


export default {
  AgendaTile,
  AgendaView,
};
