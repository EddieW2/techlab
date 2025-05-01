document.addEventListener("DOMContentLoaded", function () {
    const confirmPaymentBtn = document.getElementById("confirmPayment");
    const totalPrice = parseFloat(document.getElementById("totalPrice").innerText);
    let walletBalance = parseFloat(document.getElementById("walletBalance").innerText);
    const errorMessage = document.getElementById("errorMessage");

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    confirmPaymentBtn.addEventListener("click", function () {
        if (walletBalance < totalPrice) {
            errorMessage.innerText = "Insufficient funds!";
            return;
        }

        confirmPaymentBtn.disabled = true;
        confirmPaymentBtn.innerText = "Processing...";

        fetch("/process-payment/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ total_price: totalPrice })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Payment Successful!");
                window.location.href = thankYouUrl;
            } else {
                errorMessage.innerText = data.error || "An error occurred. Please try again.";
                confirmPaymentBtn.disabled = false;
                confirmPaymentBtn.innerText = "Confirm Payment";
            }
        })
        .catch(error => {
            console.error("Error processing payment:", error);
            errorMessage.innerText = "Network error. Please try again.";
            confirmPaymentBtn.disabled = false;
            confirmPaymentBtn.innerText = "Confirm Payment";
        });
        
    });
});