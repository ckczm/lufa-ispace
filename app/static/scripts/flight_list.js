$(function () {
    $('#create_flight_button').click(function(event){
        event.preventDefault();
        console.log('elo');
        var flight_no_input = document.getElementById('flight-no-input').value;
        var url = '/get_flight/' + flight_no_input;
        $.getJSON(url, function(data){
            console.log(data);
            if(data == null){
                document.getElementById('create_flight_form').submit();
            }
            else{
                $("#response").animate({
                    height: '+=72px'
                }, 300);
                $('<div class="alert alert-danger">' +
                    '<button type="button" class="close" data-dismiss="alert">' +
                    '&times;</button>Flight already exist! Set new flight' + 
                    'number.</div>').hide().appendTo('#response').fadeIn(1000);

                $(".alert").delay(3000).fadeOut(
                    "normal",
                    function(){
                        $(this).remove();
                });

                $("#response").delay(4000).animate({
                    height: '-=72px'
                }, 300);
            }
        });
    })
})

$(function() {
    $("#delete_flight_button").on('click', function(event){
        event.preventDefault();
        flight_num = document.getElementById('delete_flight_title').textContent.split(' ')[2]

        $.post('/delete_flight', {
            flight_no: flight_num
        })

        var row_id = 'flight_row_' + flight_num;
        document.getElementById(row_id).remove();
    });
})

$(function() {
    $('#delete_flight_modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var flight_no = button.data('flight') // Extract info from data-* attributes
        // Update the modal's content
        var modal = $(this) 
        modal.find('.modal-title').text('Delete flight ' + flight_no + ' ?')
    });
})
