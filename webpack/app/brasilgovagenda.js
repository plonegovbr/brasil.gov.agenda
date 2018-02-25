import AgendaTile from './js/tile.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
  for (let tile of $('.agenda-tile')) {
    new AgendaTile(tile);
  }
});


export default {
  AgendaTile,
};
