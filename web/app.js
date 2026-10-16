const pets = [...document.querySelectorAll('.pet')].map((element, index) => ({
  element,
  sticker: element.querySelector('.pat-sticker'),
  phase: index === 0 ? 0 : 1.7,
  pausedUntil: 0,
  frozen: { x: 0, y: 0, rotation: 0 },
  resumeTimer: null,
}));

const motionAt = (time, phase) => ({
  x: Math.cos((time + phase) * 1.4) * 3,
  y: Math.sin((time + phase) * 2.2) * 10,
  rotation: Math.sin((time + phase) * 1.4) * 2,
});

const showSticker = (pet) => {
  pet.sticker.classList.remove('is-visible');
  void pet.sticker.offsetWidth;
  pet.sticker.classList.add('is-visible');
};

pets.forEach((pet) => {
  pet.element.addEventListener('click', () => {
    const now = performance.now() / 1000;
    if (pet.pausedUntil <= now) pet.frozen = motionAt(now, pet.phase);
    pet.pausedUntil = now + 2;
    clearTimeout(pet.resumeTimer);
    showSticker(pet);
    pet.resumeTimer = setTimeout(() => pet.sticker.classList.remove('is-visible'), 2000);
  });
});

const render = (timestamp) => {
  const time = timestamp / 1000;
  pets.forEach((pet) => {
    const paused = pet.pausedUntil > time;
    const motion = paused ? pet.frozen : motionAt(time, pet.phase);
    pet.element.style.transform = `translate3d(calc(-50% + ${motion.x}px), calc(-50% + ${motion.y}px), 0) rotate(${motion.rotation}deg)`;
  });
  requestAnimationFrame(render);
};

requestAnimationFrame(render);

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
}
