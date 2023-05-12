  $(document).ready(function() {
  // Handle edit word button click
  $('.edit-word-btn').click(function() {
    var wordId = $(this).data('word-id');
    var word = $(this).data('word-text');
    var trans = $(this).data('word-translation');
    console.log(wordId,word,trans);
    // TODO: Display word data in modal form
  });
});

$('.sort-btn').click(function() {
  const column = $(this).data('sort');
  const reverse = $(this).hasClass('sort-desc');
  sortWordsBy(column, reverse);
  $(this).toggleClass('sort-desc');
});


function sortWordsBy(column, reverse) {
  const rows = Array.from(document.querySelectorAll('tbody tr'));
  const sortedRows = rows.sort((a, b) => {
    const aData = a.querySelector(`.word-${column}`).textContent.trim();
    const bData = b.querySelector(`.word-${column}`).textContent.trim();
    if (aData < bData) {
      return reverse ? 1 : -1;
    } else if (aData > bData) {
      return reverse ? -1 : 1;
    } else {
      return 0;
    }
  });
  const tableBody = document.querySelector('tbody');
  tableBody.innerHTML = '';
  sortedRows.forEach(row => tableBody.appendChild(row));
}

