$(document).ready(function() {
    // Function to update the map on the frontend
    function updateMap(data) {
        $('#map-container').empty();
        for (let i = 0; i < data.grid.length; i++) {
            for (let j = 0; j < data.grid[i].length; j++) {
                let cellClass = 'grid-cell';
                if (i == data.vehicle_position[0] && j == data.vehicle_position[1]) {
                    cellClass += ' V';
                } else if (i == data.goal_position[0] && j == data.goal_position[1]) {
                    cellClass += ' G';
                } else if (data.grid[i][j] == 'X') {
                    cellClass += ' X';
                }
                $('#map-container').append(`<div class="${cellClass}">${data.grid[i][j]}</div>`);
            }
        }
    }

    // Function to move the vehicle
    function moveVehicle() {
        $.ajax({
            type: 'POST',
            url: '/move_vehicle',
            success: function(response) {
                if (response.success) {
                    getMap();  // Update the map after moving the vehicle
                }
            }
        });
    }

    // Function to get the initial map
    function getMap() {
        $.ajax({
            type: 'GET',
            url: '/get_map',
            success: function(response) {
                updateMap(response);
            }
        });
    }

    // Initial setup
    getMap();

    // Move the vehicle on button click
    $('#move-btn').click(function() {
        moveVehicle();
    });
});
