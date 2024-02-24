get_element_selector = (target) => {
    const tag_selector = target.tagName.toLowerCase();
    const classes = target.className.split(' ');
    let cls_selector = '';
    classes.forEach(cls => {
        if (cls.trim().length == 0) {
            return;
        }
        cls_selector += '.' + cls;
    })
    const id_selector = event.id ? ('#' + event.id) : '';

    let attr_selector = '';
    for (let i = 0; i < target.attributes.length; i++) {
        const attr = target.attributes.item(i)
        if (attr.name == 'id' || attr.name == 'class') {
            continue
        }
        attr_selector += '[' + attr.name + '="' + attr.value + '"]';
    }

    let index_selector = '';
    if (target.parentNode.children.length > 1) {
        const index = Array.from(target.parentNode.children).indexOf(target) + 1;
        index_selector = ":nth-child(" + index.toString() + ")";
    }
    // Should count last of type

    selector = tag_selector + id_selector + cls_selector + attr_selector + index_selector;

    return selector;
}
getSelectorToRoot = (target) => {
    let selector = "";

    selector += get_element_selector(target);
    target = target.parentNode;
    while (target) {
        if (!target.tagName) {
            if (!target.host) {
                break
            }
            // If shadow root
            target = target.host;
        }
        selector = get_element_selector(target) + '>' + selector;
        target = target.parentNode;
    }

    return selector;
}
addEventListener('click', (event) => {
    // Try to get the original target, even if in shadow DOM
    const timestamp = event.timeStamp;
    const target = event.composedPath()[0];
    const selector = getSelectorToRoot(target);

    console.log(_keystr01238 + JSON.stringify({"event": "click", timestamp, selector}))
});

addEventListener('keypress', (event) => {
    const charCode = event.charCode;
    const timestamp = event.timeStamp;
    const target = event.composedPath()[0];
    const selector = getSelectorToRoot(target);
    const value = target.value;

    console.log(_keystr01238 + JSON.stringify({"event": "keypress", timestamp, selector, value, charCode}));
});

addEventListener('input', (event) => {
    const target = event.composedPath()[0];
    const selector = getSelectorToRoot(target);
    const value = target.value;
    const timestamp = event.timeStamp;

    console.log(_keystr01238 + JSON.stringify({"event": "input", timestamp, selector, value}));
});

