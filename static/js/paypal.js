
window.paypal_sdk
  .Buttons({
    // ------------------

    createOrder: function(data, actions){
      return actions.order.create({
        purchase_units:[{
          amount:{
            value: amount,
          }
        }]
      });
    },
    onApprove: function(data, actions){
      return actions.order.capture().then(function(details){
        sendData()

        function sendData(){
          fetch(url, {
            method : "POST",
            headers: {
              'Access-Control-Allow-Origin': '*' ,
              'Content-type': 'application/json',
              "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
              orderID: orderId,
              transID: details.id,
              paymentMethod: paymentMethod,
              status: details.status,
            }),

          })
          .then(response => response.json())
          .then(data => {
            window.location.href = order_complete_url +'?order_number='+data.order_number+'&payment_id='+data.payment_id
          })
        }
      });
    }
    
  })
  .render("#paypal-button-container");

// Example function to show a result to the user. Your site's UI library can be used instead.
function resultMessage(message) {
  const container = document.querySelector("#result-message");
  container.innerHTML = message;
}