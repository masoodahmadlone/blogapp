document.addEventListener("DOMContentLoaded", function () {
  
  // Initial WebSocket connection
  connectWebSocket();

  // Function to connect the WebSocket
  function connectWebSocket() {
    notificationSocket = createWebSocket();
  }

  // Function to create a WebSocket connection
  function createWebSocket() {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

    // Set up event handlers
    socket.onmessage = onMessage;
    socket.onerror = onError;
    socket.onclose = onClose;

    return socket;
  }

  // Handle incoming messages
  function onMessage(e) {
    const data = JSON.parse(e.data);
    console.log('Notification received:', data.message);
    displayNotification(data.message);
  }

  // Handle WebSocket errors
  function onError(e) {
    console.error('WebSocket error observed:', e);
  }

  // Handle WebSocket closure
  function onClose(e) {
    console.error('WebSocket closed unexpectedly');
    // Try to reconnect
    setTimeout(reconnectWebSocket, 3000); 
  }

  // Function to display notification on the UI
  function displayNotification(message) {
    const notificationArea = document.getElementById('notification-area');
    if (!notificationArea) {
      console.error('Notification area not found');
      return;
    }
    const notificationElement = document.createElement('div');
    notificationElement.innerText = message;
    notificationElement.className = 'notification'; 
    notificationArea.appendChild(notificationElement);
  }

  // Function to reconnect WebSocket
  function reconnectWebSocket() {
    console.log('Attempting to reconnect...');
    connectWebSocket();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Sticky header on scroll
   */
  const selectHeader = document.querySelector('#header');
  if (selectHeader) {
    document.addEventListener('scroll', () => {
      window.scrollY > 100 ? selectHeader.classList.add('sticked') : selectHeader.classList.remove('sticked');
    });
  }

  /**
   * Mobile nav toggle
   */

  const mobileNavToogleButton = document.querySelector('.mobile-nav-toggle');

  if (mobileNavToogleButton) {
    mobileNavToogleButton.addEventListener('click', function(event) {
      event.preventDefault();
      mobileNavToogle();
    });
  }

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToogleButton.classList.toggle('bi-list');
    mobileNavToogleButton.classList.toggle('bi-x');
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navbar a').forEach(navbarlink => {

    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll('.navbar .dropdown > a');

  navDropdowns.forEach(el => {
    el.addEventListener('click', function(event) {
      if (document.querySelector('.mobile-nav-active')) {
        event.preventDefault();
        this.classList.toggle('active');
        this.nextElementSibling.classList.toggle('dropdown-active');

        let dropDownIndicator = this.querySelector('.dropdown-indicator');
        dropDownIndicator.classList.toggle('bi-chevron-up');
        dropDownIndicator.classList.toggle('bi-chevron-down');
      }
    })
  });

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    const togglescrollTop = function() {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
    window.addEventListener('load', togglescrollTop);
    document.addEventListener('scroll', togglescrollTop);
    scrollTop.addEventListener('click', window.scrollTo({
      top: 0,
      behavior: 'smooth'
    }));
  }

  /**
   * Hero Slider
   */
  var swiper = new Swiper(".sliderFeaturedPosts", {
    spaceBetween: 0,
    speed: 500,
    centeredSlides: true,
    loop: true,
    slideToClickedSlide: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".custom-swiper-button-next",
      prevEl: ".custom-swiper-button-prev",
    },
  });

  /**
   * Open and close the search form.
   */
  const searchOpen = document.querySelector('.js-search-open');
  const searchClose = document.querySelector('.js-search-close');
  const searchWrap = document.querySelector(".js-search-form-wrap");

  searchOpen.addEventListener("click", (e) => {
    e.preventDefault();
    searchWrap.classList.add("active");
  });

  searchClose.addEventListener("click", (e) => {
    e.preventDefault();
    searchWrap.classList.remove("active");
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

});


//document.addEventListener('DOMContentLoaded', function () {
  // Get the share button element
  //var shareButton = document.getElementById('shareButton');

  // Add click event listener to the share button
 // shareButton.addEventListener('click', function () {
    // Display the social media icons popup
   // var socialIconsPopup = document.getElementById('socialIconsPopup');
   // socialIconsPopup.style.display = 'block';
 // });

  // Get the social media share links
 // var facebookShare = document.getElementById('facebookShare');
 // var twitterShare = document.getElementById('twitterShare');
 // var whatsappShare = document.getElementById('whatsappShare');

  // Add click event listeners to social media share links
 // facebookShare.addEventListener('click', function () {
  //  shareOnFacebook();
 // });

 // twitterShare.addEventListener('click', function () {
//    shareOnTwitter();
 // });

 // whatsappShare.addEventListener('click', function () {
  //  shareOnWhatsApp();
 // });
//});


// Function to share post on Twitter
function shareOnTwitter() {
  // Get post information
  var postTitle = document.querySelector('.single-post h1').innerText;
  var postContent = document.querySelector('.single-post p').innerText;

  // Replace 'YOUR_URL' with the actual URL of your website or blog post
  var shareUrl = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(postTitle + ' - ' + postContent) +
                 '&url=http://127.0.0.1:8000/post/{{ post.pk }}/';

  // Open Twitter share dialog in a new window
  window.open(shareUrl, '_blank', 'width=600,height=400');
}

// Function to share post on WhatsApp
function shareOnWhatsApp() {
  // Get post information
  var postTitle = document.querySelector('.single-post h1').innerText;
  var postContent = document.querySelector('.single-post p').innerText;

  // Replace 'YOUR_URL' with the actual URL of your website or blog post
  var shareUrl = 'https://api.whatsapp.com/send?text=' + encodeURIComponent(postTitle + ' - ' + postContent +
                 '\nRead more: http://127.0.0.1:8000/post/{{ post.pk }}/');

  // Open WhatsApp share dialog
  window.open(shareUrl);
}

// Function to share post on Facebook
function shareOnFacebook() {
// Check if Facebook SDK is loaded
if (typeof FB !== 'undefined') {
// If SDK is loaded, use SDK method to share
var postTitle = document.querySelector('.single-post h1').innerText;
var postContent = document.querySelector('.single-post p').innerText;
var postUrl = 'http://127.0.0.1:8000/post/{{ post.pk }}/';

FB.ui({
  method: 'share',
  href: postUrl,
  quote: postTitle + ' - ' + postContent
}, function(response){});
} else {
// If SDK is not loaded, fallback to the share dialog URL method
var postTitle = document.querySelector('.single-post h1').innerText;
var postContent = document.querySelector('.single-post p').innerText;

var shareUrl = 'https://www.facebook.com/sharer/sharer.php?u=http://127.0.0.1:8000/post/{{ post.pk }}/' +
               '&title=' + encodeURIComponent(postTitle) +
               '&description=' + encodeURIComponent(postContent);

window.open(shareUrl, '_blank', 'width=600,height=400');
}
}

// Load the Facebook SDK asynchronously
(function(d, s, id) {
var js, fjs = d.getElementsByTagName(s)[0];
if (d.getElementById(id)) return;
js = d.createElement(s); js.id = id;
js.src = "https://connect.facebook.net/en_US/sdk.js";
fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Initialize the Facebook SDK with your app ID
window.fbAsyncInit = function() {
FB.init({
appId            : 'your-app-id',
autoLogAppEvents : true,
xfbml            : true,
version          : 'v10.0'
});
};

