var ViewModel = function() {
    this.photonsPosition = ko.observable(50);
    this.size = ko.observable(256);
 
    this.imageUrl = ko.observable(null);

    this.buildUrl = function(action) {
        var size = this.size();
        return "/" + action + "/cornel-box/" + size + "x" + size + "?photons=" + this.photons();
    };
    this.render = function() {
        this.imageUrl(this.buildUrl('render'));
    };
    this.estimate = function() {
        fetch(this.buildUrl('estimate')).then(function (r) { return r.text(); }).then(console.log);
    };
    this.photons = ko.pureComputed(function() {
        // https://stackoverflow.com/questions/846221/logarithmic-slider
        // position will be between 0 and 100
        var minp = 0;
        var maxp = 100;

        // The result should be between 100 and 1000000
        var minv = Math.log(100);
        var maxv = Math.log(1000000);

        // calculate adjustment factor
        var scale = (maxv - minv) / (maxp - minp);

        var value =  Math.exp(minv + scale * (this.photonsPosition() - minp));
        return Math.round(value);        
    }, this);
};

function ready(fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

ready(function() {
    ko.applyBindings(new ViewModel());    
});
