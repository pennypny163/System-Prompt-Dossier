(() => {
  const search = document.querySelector('#personaSearch');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.persona-card')];
  const rows = [...document.querySelectorAll('.comparison-table tbody tr')];
  const count = document.querySelector('#visibleCount');
  const empty = document.querySelector('#personaEmpty');
  let activeFilter = 'all';

  const normalize = (value) => value.trim().toLocaleLowerCase('zh-CN');

  function update() {
    const query = normalize(search.value);
    const visibleModels = new Set();

    cards.forEach((card) => {
      const categories = card.dataset.categories.split(' ');
      const matchesFilter = activeFilter === 'all' || categories.includes(activeFilter);
      const matchesQuery = !query || normalize(`${card.dataset.search} ${card.textContent}`).includes(query);
      const visible = matchesFilter && matchesQuery;
      card.hidden = !visible;
      if (visible) visibleModels.add(card.dataset.model);
    });

    rows.forEach((row) => {
      row.hidden = !visibleModels.has(row.dataset.model);
    });

    count.textContent = String(visibleModels.size);
    empty.hidden = visibleModels.size !== 0;
  }

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter;
      buttons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle('active', active);
        candidate.setAttribute('aria-pressed', String(active));
      });
      update();
    });
  });

  search.addEventListener('input', update);
})();
