let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],     //geocode --> street address
                                                //establishment --> office, building addressses etc..
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},  
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){     //gets triggered once we hit the required suggestion!!!!!
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        //console.log('place name=>', place.name)
    }

    ///////////////////GOOGLE DOCUMENTATION CODE-ENDS//////////////////////



    // get the address components and assign them to the fields

    //console.log(place);

    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({ 'address': address }, function (results, status) {
        // console.log('results=>', results)
        // console.log('status=>', status)
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);

            
            //jquery
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);

        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);

    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode


            //we may not get some places with a pincode, so we handle that case by this!
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }


}


$(document).ready(function () {
   

    // add to cart
    
    $('.add_to_cart').on('click', function (e) {   //add_to_cart is the className given for (+) button
        e.preventDefault();

        food_id = $(this).attr('data-id');  //get the id of specific food
        url = $(this).attr('data-url');  

        
                                                                                            //ONCE, we click add_to_cat(+), it fetches the respective food_id and send the request to the specified url using ajax request
                                                                                            //that url, will go to add_to_cart function in views and get the response, that response is captured by the success function response
        //AJAX-REQUEST
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function(){   //info is bootstrap class
                        window.location = '/login';
                    })
                }

                else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                }
                
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);   //<label id="qty-{{food.id}}">0</label>  the id id this id

                    // subtotal, tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }

        })
    }) 


    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')    //<span id="qty-{{item.fooditem.id}}"   we are fetching this id!
        var qty = $(this).attr('data-qty')  //<span id="qty-{{item.fooditem.id}}" class="item_qty" data-qty="{{ item.quantity }}">   we are fetching this data-qty
        $('#'+the_id).html(qty)
    })



    // decrease cart
    $('.decrease_cart').on('click', function(e){   
        e.preventDefault();

        food_id = $(this).attr('data-id');  //get the id of specific food
        url = $(this).attr('data-url');  
        cart_id = $(this).attr('id');
        
                                                                                            
        //AJAX-REQUEST
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {   //info is bootstrap class
                        window.location = '/login';
                    })
                }

                else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                }
                
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);   //<label id="qty-{{food.id}}">0</label>  the id id this id


                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )


                    if (window.location.pathname == '/cart/') {    //Run this code only if this is in cart, because in marketplace, we dont have cart-id
                        removeCartItem(response.qty, cart_id);  //When clicked delete button its should not be displayed in the page
                        checkEmptyCart();               //When qty becomes 0 the item should not displayed in page

                    }
                }
            }

        })
    }) 


    // DELETE CART ITEM
    $('.delete_cart').on('click', function(e){   
        e.preventDefault();

        

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');  

        
                                                                                            
        //AJAX-REQUEST
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function(){   //info is bootstrap class
                        window.location = '/login';
                    })
                }
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, "success")

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    removeCartItem(0, cart_id);  //Delete the paritcular cart, when count == 0
                    checkEmptyCart();   //for printing Cart-empty if there is no cart, without refreshing the page
                }
            }

        })
    })


    //CALL THIS FUNCTION in delete_cart
    // delete the cart element if the qty is 0
    function removeCartItem(cartItemQty, cart_id){  //cart_id of which we are going to delete
            if(cartItemQty <= 0){
                // remove the cart item element
                document.getElementById("cart-item-"+cart_id).remove()   //remove the seleted food-item by getting its-id, which we get automatically!
            }

    }


    // Check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML   //cart_counter is the ID of the cart-logo in the top of the page
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";     //changing the display from none to block for that div
        }
    }



    // apply cart amounts
    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){  //run only in cart-page
            $('#subtotal').html(subtotal) //<span id="subtotal">0</span>
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
    }

});





