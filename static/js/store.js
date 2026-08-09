let cart =
    JSON.parse(
        localStorage.getItem("rohitHubCart") || "[]"
    );


let currentCategory = "";


const grid =
    document.getElementById(
        "productsGrid"
    );


const search =
    document.getElementById(
        "search"
    );


const sort =
    document.getElementById(
        "sort"
    );


function money(value) {

    return "₹" +
        Number(value).toLocaleString("en-IN");

}


function updateCartCount() {

    const count =
        cart.reduce(
            (total, item) =>
                total + item.quantity,
            0
        );


    document.getElementById(
        "cartCount"
    ).textContent = count;


    localStorage.setItem(
        "rohitHubCart",
        JSON.stringify(cart)
    );

}


async function loadProducts() {


    const parameters =
        new URLSearchParams();


    if (currentCategory) {

        parameters.set(
            "category",
            currentCategory
        );

    }


    if (search.value.trim()) {

        parameters.set(
            "search",
            search.value.trim()
        );

    }


    const response =
        await fetch(
            "/api/products?" +
            parameters.toString()
        );


    let products =
        await response.json();


    if (sort.value === "low") {

        products.sort(
            (a, b) =>
                a.price - b.price
        );

    }


    if (sort.value === "high") {

        products.sort(
            (a, b) =>
                b.price - a.price
        );

    }


    if (sort.value === "rating") {

        products.sort(
            (a, b) =>
                b.rating - a.rating
        );

    }


    document.getElementById(
        "resultText"
    ).textContent =
        products.length +
        " products";


    grid.innerHTML =
        products.map(
            product => `

                <article
                    class="product-card">


                    <div class="product-image">


                        <img
                            src="${product.image}"
                            alt="${product.name}"
                            loading="lazy"
                            onerror="this.src='https://placehold.co/600x600?text=Rohit+Hub'">


                    </div>


                    <div class="product-info">


                        <div class="rating">
                            ★ ${product.rating}
                        </div>


                        <h3>
                            ${product.name}
                        </h3>


                        <p>
                            ${product.category}
                        </p>


                        <div class="product-bottom">


                            <strong>
                                ${money(product.price)}
                            </strong>


                            <button
                                onclick="addToCart(${product.id})">

                                Add to Cart

                            </button>


                        </div>


                        <a
                            class="google-link"
                            href="${product.google_url}"
                            target="_blank">

                            🔎 View images on Google

                        </a>


                    </div>


                </article>

            `
        ).join("");

}


async function addToCart(productId) {


    const response =
        await fetch(
            "/api/products"
        );


    const products =
        await response.json();


    const product =
        products.find(
            item =>
                item.id === productId
        );


    if (!product) {

        return;

    }


    const existing =
        cart.find(
            item =>
                item.id === productId
        );


    if (existing) {

        existing.quantity += 1;

    } else {

        cart.push({

            id: product.id,

            name: product.name,

            price: product.price,

            image: product.image,

            quantity: 1

        });

    }


    updateCartCount();


    alert(
        product.name +
        " added to cart!"
    );

}


document
    .querySelectorAll(
        ".category-button, .category-card"
    )
    .forEach(button => {


        button.addEventListener(
            "click",
            () => {


                currentCategory =
                    button.dataset.category;


                document
                    .querySelectorAll(
                        ".category-button"
                    )
                    .forEach(item => {

                        item.classList.remove(
                            "active"
                        );

                    });


                const matching =
                    document.querySelector(
                        `.category-button[data-category="${CSS.escape(currentCategory)}"]`
                    );


                if (matching) {

                    matching.classList.add(
                        "active"
                    );

                }


                document
                    .getElementById(
                        "products"
                    )
                    .scrollIntoView({
                        behavior: "smooth"
                    });


                loadProducts();

            }
        );

    });


sort.addEventListener(
    "change",
    loadProducts
);


search.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {

            loadProducts();

        }

    }
);


updateCartCount();

loadProducts();