var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    offset: 'bottom-in-view',

    onBeforePageLoad: function () {
        $('.spinner-grow').show();
    },
    onAfterPageLoad: function () {
        $('.spinner-grow').hide();
    }
});