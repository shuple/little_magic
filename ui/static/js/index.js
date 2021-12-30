import { setMeta, setSprite } from './little_magic.js';
import { LittleMagicMake } from './little_magic_make.js';

window.addEventListener('load', function () {
  const littleMagic = new LittleMagicMake();
  const init = async function() {
    const path = 'meta/make';
    const metaData = [ `${path}/sprite`, `${path}/position`, `${path}/debug` ];
    await littleMagic.rest('/post/read',
      { 'file': metaData, 'graphic': 'sfc', 'returnData': {} }, setMeta);
    await littleMagic.rest('/post/read',
      { 'file': [ 'menu/make', 'stage/default' ], 'graphic': 'sfc', 'returnData': [] }, setSprite);
  }
  init();

  // control canvas layer
  const canvas = document.querySelector('canvas:last-child');

  // click event
  const mouseHandler = function(event) {
    event.preventDefault();
    littleMagic.mouseEvent(canvas, event);
  }  // mouseHandler()
  for (const type of [ 'click', 'contextmenu' ]) {
    canvas.addEventListener(type, mouseHandler);
  }

  // tap event, hold emulates right click
  let [ touchTimer, touchDuration ] = [ null, 300 ];
  let tapLock = false;
  const touchHandler = function(event) {
    event.preventDefault();
    tapLock = true;
    let touch = event.touches[0];
    touch.button = 2;
    littleMagic.mouseEvent(canvas, touch);
  }  // touchHandler()
  const touchStart = function(event) {
    if (event.touches.length === 1)
      touchTimer = setTimeout(touchHandler, touchDuration, event);
    else
      event.preventDefault();
  }
  const touchEnd = function(event) {
    if (tapLock) {
      event.preventDefault();
      tapLock = false;
    }
    if (touchTimer)
      clearTimeout(touchTimer);
  }
  canvas.addEventListener('touchstart', touchStart);
  canvas.addEventListener('touchend', touchEnd);

  // resize event
  const resizeHandler = function() {
    littleMagic.setGameSize();
  }
  window.addEventListener('resize', resizeHandler);
});
