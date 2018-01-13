
// https://stackoverflow.com/questions/846221/logarithmic-slider
function exponentialSlider(id, a, b) {
    // position will be between 0 and 100
    const el = document.getElementById(id);
    var minp = el.min;
    var maxp = el.max;

    // The result should be between a and b
    var minv = Math.log(a);
    var maxv = Math.log(b);

    // calculate adjustment factor
    var scale = (maxv - minv) / (maxp - minp);

    return Math.exp(minv + scale * (el.value - minp));
}

function buildUrl(action) {
    var photons = Math.round(exponentialSlider('photons', 1, 1000000));
    var size = document.getElementById('size').value;
    return "/"+action+"/cornel-box/" + size + "x" + size + "?photons=" + photons;
}

function update() {
    var target = document.getElementById('target');
    target.src = buildUrl('render');
    console.log(target.src);
}

function estimate() {
    fetch(buildUrl('estimate')).then(function (r) { return r.text(); }).then(console.log);
}