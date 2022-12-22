$('.js-vote').click(function (ev) {
    ev.preventDefault();
    let $this = $(this),
        model = $this.data('model'),
        action = $this.data('action'),
        id = $this.data('id');
    $.ajax('/vote/', {
        method: 'POST',
        data: {
            model: model,
            action: action,
            id: id
        }
    }).done(function ({'rating': rating}) {
        if (rating !== undefined) {
            document.getElementById(model + id).innerHTML = rating;
        }
    })
});