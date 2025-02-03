$(document).ready(function() {
    const dropdown = $('#player-dropdown');
    const responseContainer = $('#response');
    const newResponseContainer = $('#new-response');
    const predictionResponse = $('#prediction-response');
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

    // Fetch and display prediction results
    async function fetchPlayerPrediction(playerName) {
        try {
            const Response = await fetch(`/api/v1/player-prediction/${encodeURIComponent(playerName)}`);
            if (!Response.ok) throw new Error('Failed to fetch prediction results');

            const data = await Response.json();
            console.log('Prediction API Response:', data); // Log the full API response
            displayPredictionResults(data.result);
        } catch (error) {
            predictionResponse.html(`<strong>Error fetching prediction results: ${error.message}</strong>`);
        }
    }

    // Display prediction results
    function displayPredictionResults(result) {
        predictionResponse.empty();
        console.log('Result object:', result); // Debugging line to inspect result
        evaluation =  result >= 0.5 ? 'high' : 'low';
        predictionResponse.html(`Prospect Prediction Results: <span class="probability-value">${evaluation}</span>`);
        // if (typeof result === 'number' && !isNaN(result)) { 
        //     const formattedProb = result.toFixed(2); // Format to two decimal places
        //     predictionResponse.html(`Model Prediction Results: <span class="probability-value">${formattedProb}</span>`);
        // } else {
        //     console.log('No valid prediction result found.'); // Log if result is not as expected
        //     predictionResponse.html('<strong>No prediction results available.</strong>');
        // }
    }

    
    function populateDropdown(players) {
        players.forEach(player => {
            const option = $('<option>').val(player).text(player);
            dropdown.append(option);
        });
    }

    // Handle player selection from dropdown
    dropdown.change(function() {
        const selectedPlayer = $(this).val();
        if (selectedPlayer) {
            fetchPlayerData(selectedPlayer).then(() => {
                fetchPlayerDataAndCompare(selectedPlayer);
                fetchPlayerPrediction(selectedPlayer); // Fetch prediction results
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


            const newInjuriesHeader = $('<div>', { class: 'table-title' }).text('Injuries For Last 5 Years');
           //const newInjuries = data.new_injuries ? data.new_injuries[0] : {};
           const newInjuries = {
            Injury_Count: stats.Injury_Count || 0,
            Total_DL_Length: stats.Total_DL_Length || 0
            };
        
           const newInjuriesTable = createNewInjuriesTable('Injuries', newInjuries);
            newResponseContainer.append(newInjuriesHeader).append(newInjuriesTable);

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
                // if (newResponseContainer.children().length > 0) {
                //     console.log('Appending newResponseContainer to comparisonResponse');
                //     comparisonResponse.append(newResponseContainer.clone());
                // }
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

        const sportIdMappings = {
            11: "AAA",
            12: "AA",
            13: "A+",
            14: "A"
        };
        
        function mapMetricValue(metric, value) {
            // Specific handling for Sport_id
            if (metric === "Sport_id") {
                return sportIdMappings[value] || value;
            }
            // General mapping for other metrics
            if (typeof value === 'string') {
                const parts = value.split(' ');
                if (parts.length === 2 && metricMappings.hasOwnProperty(parts[1])) {
                    return `${parts[0]} ${metricMappings[parts[1]]}`;
                }
            }
            return value;
        }

        orderedMetrics.forEach(metric => {
            if (metrics.hasOwnProperty(metric)) {
                const mappedValue = mapMetricValue(metric, metrics[metric]);
                const row = $('<tr>')
                    .append($('<td>').text(metric))
                    .append($('<td>').text(mappedValue));
                table.append(row);
            }
        });

        // orderedMetrics.forEach(metric => {
        //     if (metrics.hasOwnProperty(metric)) {
        //         const row = $('<tr>')
        //             .append($('<td>').text(metric))
        //             .append($('<td>').text(metrics[metric]));
        //         table.append(row);
        //     }
        // });

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