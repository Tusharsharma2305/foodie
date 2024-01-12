const imgSource = "images/food-menu-1.png";

const listItem = ` <li>
<div class="food-menu-card">
  <div class="card-banner">
    <img
      src="${imgSource}"
      width="300"
      height="300"
      loading="lazy"
      alt="{{imgAlt}}"
      class="w-100"
    />

    <div class="badge">-15%</div>

    <button class="btn food-menu-btn" onclick="addToCart({{pk}})" >Add To Cart</button>
  </div>

  <div class="wrapper">
    <p class="category">{{title}}</p>

    <div class="rating-wrapper">
      <ion-icon name="star"></ion-icon>
      <ion-icon name="star"></ion-icon>
      <ion-icon name="star"></ion-icon>
      <ion-icon name="star"></ion-icon>
      <ion-icon name="star"></ion-icon>
    </div>
  </div>

  <h3 class="h3 card-title">{{feature}}</h3>

  <div class="price-wrapper">
    <p class="price-text">Price:</p>

    <data class="price">{{price}}</data>

    <del class="del" value="{{price}}">{{price}}</del>
  </div>
</div>
</li>
`


$(document).ready(function(){

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'INR',
      });

    console.log(foodItems);
    foodItems.forEach(item => {
        let it = listItem
            .replaceAll("{{price}}",formatter.format(item.fields.price))
            .replaceAll("{{title}}",item.fields.food_title)
            .replaceAll("{{imgSource}}",item.fields.img_name)
            .replaceAll("{{imgAlt}}",item.fields.food_title)
            .replaceAll("{{feature}}",item.fields.feature)
            .replaceAll("{{pk}}",item.pk)
        $("#food-items-list").append(it)
    });

    $(`#category-${category}`).addClass('active');
    console.log(`#category-${category}`);

});


function addToCart(food_id) {
  // Check if the user is authenticated
  $.ajax({
      url: '/check_authentication/',  // Create a Django view to check authentication
      type: 'GET',
      success: function(response) {
          if (response.authenticated) {
              // User is authenticated, proceed with adding to cart
              console.log(response.authenticated)
              $.ajax({
                  url: `/cart/${food_id}`,
                  success: function(result) {
                      console.log(result);
                      Swal.mixin({
                          toast: true,
                          position: 'top-end',
                          showConfirmButton: false,
                          timer: 3000,
                      }).fire({
                          icon: 'success',
                          title: 'Added To Cart',
                      });
                  },
              });
          } else {
              // User is not authenticated, show login message
              Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
            }).fire({
                icon: 'error',
                title: 'login first',
            });
          }
      },
  });
}
