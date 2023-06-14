document.addEventListener('DOMContentLoaded', function() {
    // these were added to avoid null values in certain pages
    var registering = document.querySelector('.register')
    var logining = document.querySelector('.login')
    
    if (registering != null) {
        register();
    }   
    if (logining != null){
        login();
    }
    // this form should make a new card in my_listed_items.html but it doesn't
    var sell_form = document.querySelector('.sell-form');
    if (sell_form != null) {
        sell();
    }
    // this is to change the navbar depending on the user type
    // var userType = localStorage.getItem("userType");
    // if (userType != null) {
    // }
    
});
function register() {
    var reg = document.querySelector('.register')
    var form = document.querySelector('.reg-form')
    var artist = document.getElementById('artist')
    var buyer = document.getElementById('buyer')
    var registerForm = document.getElementById('register-form')


    artist.addEventListener('click', function() {
        reg.style.display = 'none'
        form.style.display = 'block'
        localStorage.setItem("userType", "artist");
        registerForm.action = "/register/artist";

    });
    buyer.addEventListener('click', function() {
            reg.style.display = 'none'
            form.style.display = 'block'
            localStorage.setItem("userType", "customer");
            registerForm.action = "/register/customer";

    });
}
function login() {
    var log = document.querySelector('.login')
    var form = document.querySelector('.login-form')
    var artist = document.getElementById('artist')
    var buyer = document.getElementById('buyer')
    var loginForm = document.getElementById('login-form')

    artist.addEventListener('click', function() {
        log.style.display = 'none'
        form.style.display = 'block'
        localStorage.setItem("userType", "artist");
        loginForm.action = "/login/artist";
    });
    buyer.addEventListener('click', function() {
        log.style.display = 'none'
        form.style.display = 'block'
        localStorage.setItem("userType", "customer");
        loginForm.action = "/login/customer";
    });
}
function sell() {
  const form = document.querySelector('.sell-form');
  const submitBtn = document.querySelector('#submit-btn');
  const cardContainer = document.querySelector('#card-container');
}


