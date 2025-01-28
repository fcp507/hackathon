$(document).ready(function() {
    const dropdown = $('#player-dropdown');
    const responseContainer = $('#response');
    const newResponseContainer = $('#new-response');
    const comparisonResponse = $('#comparison-response');
    const headshotContainer = $('#headshot-container');

    async function fetchPlayers() {
        try {
            const response = await fetch('/api/v1/players');
            if (!response.ok) throw new Error('Failed to fetch player names');
            const data = await response.json();
            if (Array.isArray(data.names)) {
                populateDropdown(data.names);
            } else {
                console.error('API response is not an array:', data.names);
            }
        } catch (error) {
            console.error('Error fetching players:', error);
        }
    }

    function populateDropdown(players) {
        players.forEach(player => {
            const option = $('<option>').val(player).text(player);
            dropdown.append(option);
        });
    }

    dropdown.change(function() {
        const selectedPlayer = $(this).val();
        if (selectedPlayer) {
            fetchPlayerData(selectedPlayer).then(() => {
                fetchPlayerDataAndCompare(selectedPlayer);
            });
        }
    });

    async function fetchPlayerData(playerName) {
        try {
            const response = await fetch(`/api/v1/player-stats/${encodeURIComponent(playerName)}`);
            if (!response.ok) throw new Error('Failed to fetch player data');

            const data = await response.json();
            displayPlayerData(data);
        } catch (error) {
            responseContainer.html(`<strong>Error fetching player data: ${error.message}</strong>`);
        }
    }

    function displayPlayerData(data) {
        console.log('Displaying player data:', data);
        responseContainer.empty();
        newResponseContainer.empty();
        headshotContainer.empty();

        if (data.stats && data.stats.length > 0) {
            const stats = data.stats[0];

            if (stats.headshot_url) {
                const img = $('<img>', {
                    src: stats.headshot_url,
                    alt: `${stats.Relinqiushed || 'Player'} Headshot`,
                    class: 'player-headshot'
                });
                headshotContainer.append(img);
            }

            const statsTable = createStatsTable('Stats', stats);
            responseContainer.append(statsTable);

            //const newInjuries = data.Injury_Count ? data.new_injuries[0] : {};
            //console.log('New Injuries Data:', newInjuries);

            //  // Always create the table when newInjuries is an object
            // if (newInjuries && typeof newInjuries === 'object') {
            //     const newInjuriesHeader = $('<div>', { class: 'table-title' }).text('Injuries For Last 5 Years');
            //     const newInjuriesTable = createNewInjuriesTable('Injuries', newInjuries);
            //     newResponseContainer.append(newInjuriesHeader).append(newInjuriesTable);
            //     console.log('New Injuries Table HTML:', newResponseContainer.html());
            // } else {
            //     console.log('No injuries data available.');
            // }
            const newInjuries = data.new_injuries ? data.new_injuries[0] : {};
            const newInjuriesTable = createNewInjuriesTable('Additional Injuries', newInjuries);
            newResponseContainer.append(newInjuriesTable).append(newInjuriesTable);

        } else {
            responseContainer.append('<strong>No stats available for this player.</strong>');
        }
    }

    async function fetchPlayerDataAndCompare(playerName) {
        try {
            const response = await fetch(`/api/v1/compare-players/${encodeURIComponent(playerName)}`);
            if (!response.ok) throw new Error('Failed to fetch comparison data');

            const data = await response.json();
            displayComparison(data.result);
        } catch (error) {
            comparisonResponse.html(`<strong>Error comparing players: ${error.message}</strong>`);
        }
    }

    function displayComparison(data) {
        console.log('Displaying comparison data:', data);
        comparisonResponse.empty();

        if (data) {
            const comparisonTitle = $('<div>', { class: 'table-title' }).text('The Closest Major Team Player');
            const comparisonMetrics = data.closest_major_player_metrics || {};

            const filteredMetrics = filterValidMetrics(comparisonMetrics);

            if (Object.keys(filteredMetrics).length > 0) {
                const comparisonTable = createStatsTable(data.closest_major_player || 'Closest Match', filteredMetrics);
                const similarityScore = $('<div>', { class: 'similarity-score' }).text(`Similarity Score: ${data.similarity_score.toFixed(4)}`);
                
                comparisonResponse.append(comparisonTitle).append(comparisonTable).append(similarityScore);

                // Ensure newResponseContainer is appended after it's populated
                if (newResponseContainer.children().length > 0) {
                    console.log('Appending newResponseContainer to comparisonResponse');
                    comparisonResponse.append(newResponseContainer.clone());
                }
            } else {
                comparisonResponse.append('<strong>No relevant comparison data available.</strong>');
            }
        } else {
            comparisonResponse.append('<strong>No data available for comparison.</strong>');
        }
    }

    function filterValidMetrics(metrics) {
        const validMetrics = {};
        for (const metric in metrics) {
            if (metrics[metric] !== undefined && metrics[metric] !== 'N/A') {
                validMetrics[metric] = metrics[metric];
            }
        }
        return validMetrics;
    }

    function createStatsTable(playerName, metrics) {
        const table = $('<table>', { class: 'stats-table' });
        const headerRow = $('<tr>')
            .append($('<th>').text('Metric'))
            .append($('<th>').text(playerName));
        table.append(headerRow);

        const orderedMetrics = [
            "Sport_id", "currentAge", "height", "weight", "draftYear",
            "strikeZoneTop", "strikeZoneBottom", "W", "L", "G", "GS", "GF",
            "CG", "QS", "SHO", "SVO", "SV", "HLD", "BS", "IP_str", "IP", "BF",
            "AB", "R", "H", "Double_B", "Triple_B", "R2", "ER", "HR", "TB",
            "BB", "IBB", "SO", "HBP", "BK", "GiDP", "GiDP_opp", "CI", "IR",
            "IRS", "BqR", "BqRS", "RS", "SF", "SB", "CS", "PK", "FH", "PH",
            "LH", "FO", "GO", "AO", "pop_outs", "line_outs", "PI",
            "total_swings", "swing_and_misses", "balls_in_play", "PI_strikes",
            "PI_balls", "WP", "W_perc", "ERA", "RA9", "WHIP", "H_9", "HR_9",
            "BB_9", "SO_9", "BABiP", "SO_BB", "BA", "OBP", "SLG", "SO_perc",
            "BB_SO", "PI_PA", "HR_PA", "BB_PA", "PI_IP"
        ];

        orderedMetrics.forEach(metric => {
            if (metrics.hasOwnProperty(metric)) {
                const row = $('<tr>')
                    .append($('<td>').text(metric))
                    .append($('<td>').text(metrics[metric]));
                table.append(row);
            }
        });

        return table;
    }

    function createNewInjuriesTable(title, newInjuries) {
        const table = $('<table>', { class: 'stats-table' });
        const headerRow = $('<tr>').append($('<th>').text('Metric'))
                                   .append($('<th>').text(title));
        table.append(headerRow);

        const metrics = ['Injury_Count', 'Total_DL_Length'];
        metrics.forEach(metric => {
            const value = newInjuries[metric] !== undefined ? newInjuries[metric] : 0;
            const row = $('<tr>').append($('<td>').text(metric))
                                 .append($('<td>').text(value));
            table.append(row);
        });

        return table;
    }

    fetchPlayers();
});