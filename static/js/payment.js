let cart =
    JSON.parse(
        localStorage.getItem("rohitHubCart") || "[]"
    );


function money(value) {

    return "₹" +
        Number(value).toLocaleString("en-IN");

}


const total =
    cart.reduce(
        (sum, item) =>
            sum +
            item.price *
            item.quantity,
        0
    );


document.getElementById(
    "paymentTotal"
).textContent =
    money(total);


const paymentFields =
    document.getElementById(
        "paymentFields"
    );


function showPaymentFields() {


    const selected =
        document.querySelector(
            'input[name="payment"]:checked'
        ).value;


    if (selected === "upi") {

        paymentFields.innerHTML = `

            <input
                id="upiId"
                placeholder="UPI ID (Demo)">

        `;

    }


    if (selected === "card") {

        paymentFields.innerHTML = `

            <input
                placeholder="Card Number (Demo)"
                maxlength="19">

            <div class="form-grid">

                <input
                    placeholder="MM / YY">

                <input
                    placeholder="CVV">

            </div>

        `;

    }


    if (selected === "cod") {

        paymentFields.innerHTML = `

            <div class="cod-box">

                <strong>
                    Cash on Delivery
                </strong>

                <br><br>

                Pay when your Rohit Hub
                order is delivered.

            </div>

        `;

    }

}


document
    .querySelectorAll(
        'input[name="payment"]'
    )
    .forEach(
        input => {

            input.addEventListener(
                "change",
                showPaymentFields
            );

        }
    );


document
    .getElementById(
        "payButton"
    )
    .addEventListener(
        "click",
        () => {


            if (cart.length === 0) {

                alert(
                    "Your cart is empty."
                );

                window.location.href =
                    "/";

                return;

            }


            const selected =
                document.querySelector(
                    'input[name="payment"]:checked'
                ).value;


            if (
                selected === "upi"
            ) {

                const upi =
                    document.getElementById(
                        "upiId"
                    );


                if (
                    !upi ||
                    !upi.value.trim()
                ) {

                    alert(
                        "Please enter a demo UPI ID."
                    );

                    return;

                }

            }


            localStorage.removeItem(
                "rohitHubCart"
            );


            window.location.href =
                "/order-success";

        }
    );


showPaymentFields();