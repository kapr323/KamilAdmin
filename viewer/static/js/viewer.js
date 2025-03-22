function showSubtiles(sectionId) {
    document.querySelector('#main-tiles').style.display = 'none';
    document.querySelector('#subtiles').style.display = 'block';
    document.querySelectorAll('#subtiles .tiles').forEach(group => {
        group.style.display = 'none';
    });

    const target = document.querySelector(`#${sectionId}`);
    if (target) {
        target.style.display = 'grid';
    }
}

function backToMain() {
    document.querySelector('#subtiles').style.display = 'none';
    document.querySelector('#main-tiles').style.display = 'grid';
    document.querySelectorAll('#subtiles .tiles').forEach(group => {
        group.style.display = 'none';
    });
}
