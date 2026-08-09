let cart =
    JSON.parse(
        localStorage.getItem("rohitHubCart") || "[]"
    );


const items =
    document.getElementById(
        "checkoutItems"
    );


const totalElement =
    document.getElementById(
        "checkoutTotal"
    );


function money(value) {

    return "₹" +
        Number(value).toLocaleString("en-IN");

}


function renderCart() {


    if (cart.length === 0) {

        items.innerHTML = `

            <p>
                Your cart is empty.
            </p>

            <br>

            <a href="/">
                ← Shop Products
            </a>

        `;


        totalElement.textContent =
            "₹0";


        return;

    }


    items.innerHTML =
        cart.map(
            (item, index) => `

                <div
                    class="cart-item">


                    <img
                        class="cart-image"
                        src="${item.image}"
                        alt="${item.name}">


                    <div>

                        <strong>
                            ${item.name}
                        </strong>

                        <small>

                            ${item.quantity}
                            ×
                            ${money(item.price)}

                        </small>

                    </div>


                    <strong>

                        ${money(
                            item.price *
                            item.quantity
                        )}

                    </strong>


                    <button
                        onclick="removeItem(${index})">

                        ×

                    </button>


                </div>

            `
        ).join("");


    const total =
        cart.reduce(
            (sum, item) =>
                sum +
                item.price *
                item.quantity,
            0
        );


    totalElement.textContent =
        money(total);

}


function removeItem(index) {


    cart.splice(
        index,
        1
    );


    localStorage.setItem(
        "rohitHubCart",
        JSON.stringify(cart)
    );


    renderCart();

}


document
    .getElementById(
        "checkoutForm"
    )
    .addEventListener(
        "submit",
        event => {


            event.preventDefault();


            if (cart.length === 0) {

                alert(
                    "Your cart is empty."
                );

                return;

            }


            const customer =
                Object.fromEntries(
                    new FormData(
                        event.target
                    )
                );


            localStorage.setItem(
                "rohitHubCustomer",
                JSON.stringify(customer)
            );


            window.location.href =
                "/payment";

        }
    );


renderCart();