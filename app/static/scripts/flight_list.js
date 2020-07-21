$(function () {
    $('#create_flight_button').click(function(event){
        event.preventDefault();
        var airline = document.getElementById('airline_input').value;
        var flight_no = document.getElementById('flight-no-input').value;
        var departure = document.getElementById('departure_input').value;
        var destination = document.getElementById('destination_input').value;
        var registration = document.getElementById('registration_input').value;

        var url = '/get_flight/' + flight_no;
        $.getJSON(url, function(data){
            if(data == null){
                if(airline !== '' && departure !== '' && destination !== '' && registration !== ''){
                    document.getElementById('create_flight_form').submit();
                }
                else{
                    $("#response").animate({
                        height: '+=72px'
                    }, 300);
                    $('<div class="alert alert-danger">' +
                        '<button type="button" class="close" data-dismiss="alert">' +
                        '&times;</button>Enter all data!</div>').hide().appendTo('#response').fadeIn(1000);
    
                    $(".alert").delay(3000).fadeOut(
                        "normal",
                        function(){
                            $(this).remove();
                    });
    
                    $("#response").delay(4000).animate({
                        height: '-=72px'
                    }, 300);
                }
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

$(function() {
    $("#calculate_flight_button").on('click', function(event){
        event.preventDefault();
        flight_num = document.getElementById('calculate_flight_title').textContent.split(' ')[2]
        space_etops = document.getElementById('space_etops_checkbox').checked
        fuel_policy = document.getElementById('fuel_policy_checkbox').checked

        $.post('/calculate_flight', {
            flight_no: flight_num,
            etops: space_etops,
            fuel_policy: fuel_policy
        })

        var flight_status = 'flight_' + flight_num + '_status';
        document.getElementById(flight_status).textContent = 'In progress';
        document.getElementById(flight_status).className = "badge badge-info";
    });
})

$(function() {
    $('#calculate_flight_modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var flight_no = button.data('flight') // Extract info from data-* attributes
        // Update the modal's content
        var modal = $(this) 
        modal.find('.modal-title').text('Calculate flight ' + flight_no)
    });
})