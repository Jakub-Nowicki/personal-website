// app/static/js/github-calendar.js
document.addEventListener('DOMContentLoaded', function() {
    const username = 'Jakub-Nowicki'; // Your GitHub username
    const calendarContainer = document.getElementById('github-calendar');
    const loadingMessage = document.querySelector('.loading-message');

    if (!calendarContainer) return;

    fetchGitHubData(username)
        .then(renderCalendar)
        .catch(displayError);

    function fetchGitHubData(username) {
        return fetch(`/api/github-contributions/${username}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`GitHub API error: ${response.status}`);
                }
                return response.json();
            });
    }

    function renderCalendar(data) {
        if (loadingMessage) {
            loadingMessage.style.display = 'none';
        }

        if (!data || !data.contributions || !data.contributions.length) {
            displayError(new Error('No contribution data available'));
            return;
        }

        // Clear any previous calendar
        calendarContainer.innerHTML = '';

        // Create the calendar grid
        const calendarEl = document.createElement('div');
        calendarEl.className = 'github-calendar-grid';

        // Create month labels
        const monthLabels = createMonthLabels();
        calendarEl.appendChild(monthLabels);

        // Create week rows
        const weeksContainer = document.createElement('div');
        weeksContainer.className = 'github-calendar-weeks';

        // Create day labels (Mon, Wed, Fri)
        const dayLabels = createDayLabels();
        weeksContainer.appendChild(dayLabels);

        // Add contribution data
        data.contributions.forEach((week, weekIndex) => {
            const weekEl = document.createElement('div');
            weekEl.className = 'github-calendar-week';

            week.forEach((level, dayIndex) => {
                const dayEl = document.createElement('div');
                dayEl.className = `github-calendar-day level-${level}`;
                dayEl.title = `${getRelativeDate(weekIndex, dayIndex)}: ${getContributionText(level)}`;
                weekEl.appendChild(dayEl);
            });

            weeksContainer.appendChild(weekEl);
        });

        calendarEl.appendChild(weeksContainer);
        calendarContainer.appendChild(calendarEl);

        // Add legend
        const legend = createLegend();
        calendarContainer.appendChild(legend);
    }

    function createMonthLabels() {
        const monthsEl = document.createElement('div');
        monthsEl.className = 'github-calendar-months';

        // Calculate month positions based on current date
        const now = new Date();
        const months = [];

        // Go back 1 year from now
        for (let i = 12; i >= 0; i--) {
            const date = new Date();
            date.setMonth(now.getMonth() - i);
            months.push(date);
        }

        // Get unique months in the range
        const uniqueMonths = months.filter((month, index, array) => {
            return array.findIndex(m => m.getMonth() === month.getMonth()) === index;
        });

        // Create month labels
        uniqueMonths.forEach(month => {
            const monthEl = document.createElement('div');
            monthEl.className = 'github-calendar-month';
            monthEl.textContent = month.toLocaleString('default', { month: 'short' });
            monthsEl.appendChild(monthEl);
        });

        return monthsEl;
    }

    function createDayLabels() {
        const daysEl = document.createElement('div');
        daysEl.className = 'github-calendar-days';

        const days = ['Mon', '', 'Wed', '', 'Fri', ''];
        days.forEach(day => {
            const dayEl = document.createElement('div');
            dayEl.className = 'github-calendar-day-label';
            dayEl.textContent = day;
            daysEl.appendChild(dayEl);
        });

        return daysEl;
    }

    function createLegend() {
        const legendEl = document.createElement('div');
        legendEl.className = 'github-calendar-legend';

        const legendText = document.createElement('div');
        legendText.className = 'github-calendar-legend-text';
        legendText.textContent = 'Contribution activity:';
        legendEl.appendChild(legendText);

        const levels = [0, 1, 2, 3, 4];
        const legendItems = document.createElement('div');
        legendItems.className = 'github-calendar-legend-items';

        levels.forEach(level => {
            const item = document.createElement('div');
            item.className = `github-calendar-legend-item level-${level}`;
            item.title = getContributionText(level);
            legendItems.appendChild(item);
        });

        legendEl.appendChild(legendItems);
        return legendEl;
    }

    function getRelativeDate(weekIndex, dayIndex) {
        const date = new Date();
        const totalDays = (52 - weekIndex - 1) * 7 + (6 - dayIndex);
        date.setDate(date.getDate() - totalDays);
        return date.toLocaleDateString();
    }

    function getContributionText(level) {
        switch(level) {
            case 0: return 'No contributions';
            case 1: return '1-2 contributions';
            case 2: return '3-5 contributions';
            case 3: return '6-10 contributions';
            case 4: return '10+ contributions';
            default: return 'Unknown contribution level';
        }
    }

    function displayError(error) {
        console.error('GitHub calendar error:', error);

        if (loadingMessage) {
            loadingMessage.textContent = 'Could not load GitHub contribution data. Please check back later.';
            loadingMessage.style.color = '#d94f5c';
        }
    }
});