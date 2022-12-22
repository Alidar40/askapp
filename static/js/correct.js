$('.js-correct').click(function (ev) {
    ev.preventDefault()
    let $this = $(this),
        id = $this.data('id'),
        qid = $this.data('qid'),
        correct = document.getElementById('correct' + id).checked;

    $.ajax('/correct/', {
        method: 'POST',
        data: {
            id: id,
            correct: correct,
            qid: qid
        },
    }).done(function ({'correct': correct}) {
        console.log(id, correct)
        document.getElementById('correct' + id).checked = correct;
    });

})