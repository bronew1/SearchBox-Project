(function () {
  const state = { visible: false, products: [] };

  function fetchProducts() {
    fetch("https://searchprojectdemo.com/api/product/widget-products/")
      .then((res) => res.json())
      .then((data) => {
        state.products = data.products;
        renderPopup();
      });
  }

  function renderPopup() {
    const container = document.createElement("div");
    container.id = "best-seller-widget";

    const style = `
      #best-seller-toggle {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 85px;
        height: 85px;
        background-color: #ebbecb;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        z-index: 9999;
      }
      #best-seller-popup {
        position: fixed;
        bottom: 120px;
        left: 20px;
        width: 764px;
        height: 544px;
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        overflow-y: auto;
        z-index: 9999;
        display: none;
      }
      .product-card {
        width: 50%;
        padding: 12px;
        float: left;
      }
      .product-card img {
        width: 100%;
        border-radius: 8px;
        transition: transform 0.3s ease;
      }
      .product-card:hover img {
        transform: scale(1.05);
      }
    `;

    const css = document.createElement("style");
    css.innerText = style;

    const toggle = document.createElement("div");
    toggle.id = "best-seller-toggle";
    toggle.innerText = "🛍️";
    toggle.onclick = () => {
      state.visible = !state.visible;
      document.getElementById("best-seller-popup").style.display = state.visible ? "block" : "none";
    };

    const popup = document.createElement("div");
    popup.id = "best-seller-popup";
    popup.innerHTML = `
      <h2 style="text-align:center">ÇOK SATANLAR</h2>
      ${state.products
        .map(
          (p) => `
        <div class="product-card">
          <a href="${p.url}">
            <img src="${p.image_url}" alt="${p.name}" />
            <div style="text-align:center">${p.name}</div>
            <div style="text-align:center; font-weight:bold">${parseFloat(p.price).toLocaleString("tr-TR")} TL</div>
          </a>
        </div>`
        )
        .join("")}
    `;

    container.appendChild(css);
    container.appendChild(toggle);
    container.appendChild(popup);

    document.body.appendChild(container);
  }

  window.addEventListener("load", fetchProducts);
})();
