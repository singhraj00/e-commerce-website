$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



// using for plus cart 

$('.plus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            prod_id: id
        },
        success:function(data) {
          
            eml.innerText = data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount

        }

    })
})


// minus-cart 

$('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{
            prod_id: id
        },
        success:function(data) {
          
            eml.innerText = data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount

        }

    })
})


// remove cart 

$('.remove-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this 
    var epl = eml.parentNode.parentNode.parentNode.parentNode  
    console.log(epl) 
    console.log(id)
    console.log(eml)

    $.ajax({
        type:'GET',
        url:'/removecart',
        data:{
            prod_id: id
        },

        success:function(data) {
          
            console.log('delete')
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount
            // for remove

            eml.parentNode.parentNode.parentNode.parentNode.remove() 
              
        }

    })
})



// <!-- Razorpay's Javascript code. -->


 
