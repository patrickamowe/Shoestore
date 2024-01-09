
document.addEventListener('DOMContentLoaded', function () {

    const addToCartButtons = document.getElementsByClassName("add-to-cart");
    for (const addToCartButton of addToCartButtons) {

        addToCartButton.addEventListener('click', function () {
            console.log('Button clicked');
            const itemId = addToCartButton.getAttribute('data-item-id');
            console.log(itemId)
            fetch(`/add_to_cart/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Handle success
                    console.log(data.message);
                } else {
                    // Handle failure
                    console.error(data.message);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });

        });

    }


    const deleteButtons = document.getElementsByClassName("remove-item-from-cart");

    for (const deleteButton of deleteButtons) {
        deleteButton.addEventListener('click', function () {
            console.log('Button clicked');
            const itemId = deleteButton.getAttribute('data-item-id');
            fetch(`/remove_from_cart/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Handle success
                    console.log(data.message);
                    window.location.reload();
                } else {
                    // Handle failure
                    console.error(data.message);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        });
    }

    const addToWishlistButtons = document.getElementsByClassName("add-to-wishlist");
    for (const addToWishlistButton of addToWishlistButtons) {

        addToWishlistButton.addEventListener('click', function () {
            const itemId = addToWishlistButton.getAttribute('data-item-id');
            fetch(`/add_to_wishlist/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Handle success
                    console.log(data.message);
                } else {
                    // Handle failure
                    console.error(data.message, data.st);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });

        });

    }

    const removeButtons = document.getElementsByClassName("remove-item-from-wishlist");

    for (const removeButton of removeButtons) {
        removeButton.addEventListener('click', function () {
            console.log('Button clicked');
            const itemId = removeButton.getAttribute('data-item-id');
            console.log(itemId)
            fetch(`/remove_from_wishlist/${itemId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Handle success
                    console.log(data.message);
                    window.location.reload();
                } else {
                    // Handle failure
                    console.error(data.message);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        });
    }


});

