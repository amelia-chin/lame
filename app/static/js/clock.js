// Team lame (Amelia Chin, Ethan Shenker, Liam Kronman, Maddy Andersen)
// SoftDev — Rona Ed.
// P3 - Study Zone
// 2021-04-29

function updateClock() {
    var currentTime = new Date();

    var currentHours = currentTime.getHours();
    var currentMinutes = currentTime.getMinutes();
    var currentSeconds = currentTime.getSeconds();

    currentMinutes = (currentMinutes < 10 ? "0" : "") + currentMinutes;
    currentSeconds = (currentSeconds < 10 ? "0" : "") + currentSeconds;

    var timeOfDay = (currentHours < 12) ? "AM" : "PM";

    currentHours = (currentHours > 12) ? currentHours - 12 : currentHours;

    currentHours = (currentHours == 0) ? 12 : currentHours;

    var currentDay = currentTime.getDay();

    currentDay = (currentDay == 0) ? "Sun" : currentDay;
    currentDay = (currentDay == 1) ? "Mon" : currentDay;
    currentDay = (currentDay == 2) ? "Tue" : currentDay;
    currentDay = (currentDay == 3) ? "Wed" : currentDay;
    currentDay = (currentDay == 4) ? "Thu" : currentDay;
    currentDay = (currentDay == 5) ? "Fri" : currentDay;
    currentDay = (currentDay == 6) ? "Sat" : currentDay;

    var currentMonth = currentTime.getMonth( );

    currentMonth = (currentMonth == 0) ? "January" : currentMonth;
    currentMonth = (currentMonth == 1) ? "February" : currentMonth;
    currentMonth = (currentMonth == 2) ? "March" : currentMonth;
    currentMonth = (currentMonth == 3) ? "April" : currentMonth;
    currentMonth = (currentMonth == 4) ? "May" : currentMonth;
    currentMonth = (currentMonth == 5) ? "June" : currentMonth;
    currentMonth = (currentMonth == 6) ? "July" : currentMonth;
    currentMonth = (currentMonth == 7) ? "August" : currentMonth;
    currentMonth = (currentMonth == 8) ? "September" : currentMonth;
    currentMonth = (currentMonth == 9) ? "October" : currentMonth;
    currentMonth = (currentMonth == 10) ? "November" : currentMonth;
    currentMonth = (currentMonth == 11) ? "December" : currentMonth;

    var currentDate = currentTime.getDate();

    currentDate = (currentDate == 1 || currentDate == 21 || currentDate == 31) ? currentDate + "st" : currentDate;
    currentDate = (currentDate == 2 || currentDate == 22) ? currentDate + "nd" : currentDate;
    currentDate = (currentDate == 3) || currentDate == 23 ? currentDate + "rd" : currentDate;
    currentDate = (currentDate > 3 || currentDate < 21 || currentDate > 23 || currentDate < 31) ? currentDate + "th" : currentDate;

    var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay + "<br>" + currentDay + " " + currentMonth + " " + currentDate;

    document.getElementById('clock').innerHTML=currentTimeString;
}