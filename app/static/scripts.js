document.addEventListener('DOMContentLoaded', () => {
    // Copy
    var clipboard = new ClipboardJS('.btn');

    clipboard.on('success', function (e) {
        // console.info('Action:', e.action);
        // console.info('Text:', e.text);
        // console.info('Trigger:', e.trigger);
        bulmaToast.toast({
            message: 'Copiado!',
            position: 'top-right',
            type: 'is-link',
            closeOnClick: false,
            dismissible: true,
            animate: {
                in: 'fadeIn',
                out: 'fadeOut'
            },
        });
        (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
            const $notification = $delete.parentNode;

            $delete.addEventListener('click', () => {
                closeAllNotification();
            });
        });
        e.clearSelection();
    });

    clipboard.on('error', function (e) {
        console.error('Action:', e.action);
        console.error('Trigger:', e.trigger);
    });

    // Fuction close Notification
    function closeAllNotification(){
        (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
            const $notification = $delete.parentNode;
            $notification.parentNode.removeChild($notification);
        });
    }

    function closeNotification(){
        $notification.parentNode.removeChild($notification);
    }

    // Functions to open and close a modal
    function openModal($el) {
        $el.classList.add('is-active');
        document.getElementById('name').focus();
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    function closeAllDropdown() {
        (document.querySelectorAll('.dropdown') || []).forEach(($dropdown) => {
            closeDropdown($dropdown);
        });
    }

    function extendsDropdown($el) {
        $el.classList.add('is-active');
    }

    function closeDropdown($el) {
        $el.classList.remove('is-active');
    }

    function closeDropdowns() {
        $dropdowns.forEach(function ($el) {
            $el.classList.remove("is-active");
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);
        console.log($target);

        $trigger.addEventListener('click', () => {
            openModal($target);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button, .card-footer .exit') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        const e = event || window.event;

        if (e.keyCode === 27) { // Escape key
            closeAllModals();
            closeAllDropdown();
            closeAllNotification();
        }
    });

    // Add a click event on dropdown 
    (document.querySelectorAll('.target-dropdown') || []).forEach(($trigger) => {
        const dropdown = $trigger.dataset.target;
        const $target = document.getElementById(dropdown);
        console.log($target);

        $trigger.addEventListener('click', () => {
            extendsDropdown($target);
        });
    });

    // Cierra las x
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            closeAllNotification();
        });
    });


    // Cierra el dropdown si es que la cantidad es mayor que 0
    // main.js de bulma

    var $dropdowns = getAll(".dropdown, .target-dropdown");

    if ($dropdowns.length > 0) {
        $dropdowns.forEach(function ($el) {
            $el.addEventListener("click", function (event) {
                event.stopPropagation();
                $el.classList.toggle("is-active");
            });
        });

        document.addEventListener("click", function (event) {
            closeDropdowns();
        });
    }


    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }





    function getAll(selector) {
        var parent = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : document;

        return Array.prototype.slice.call(parent.querySelectorAll(selector), 0);
    }

});