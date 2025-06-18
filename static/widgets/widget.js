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
        width: 70px;
        height: 70px;
        background-color: #ebbecb;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        z-index: 9999;
        font-size: 24px;
      }

      #best-seller-popup {
        position: fixed;
        bottom: 100px;
        left: 20px;
        width: 92vw;
        max-width: 420px;
        background: white;
        border-radius: 16px;
        padding: 16px 12px;
        border: 1px solid #ebbecb;
        box-shadow: 0 2px 16px rgba(0,0,0,0.2);
        overflow-y: auto;
        max-height: 80vh;
        z-index: 9999;
        display: none;
      }

      #best-seller-popup h2 {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 12px;
      }

      .product-best-wrapper {
        width: 48%;
        float: left;
        box-sizing: border-box;
        margin: 1%;
        border: 1px solid #ebbecb;
        padding: 6px;
        border-radius: 6px;
        background: #fff;
      }

      .product-img {
        position: relative;
      }

      .base-image, .hover-image {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 6px;
      }

      .hover-image {
        position: absolute;
        top: 0;
        left: 0;
        opacity: 0;
        transition: opacity 0.3s;
      }

      .product-img:hover .hover-image {
        opacity: 1;
      }

      .hover-img-detail {
        position: absolute;
        bottom: 6px;
        left: 6px;
        color: white;
        font-size: 10px;
      }

      .product-code {
        background: rgba(0,0,0,0.6);
        padding: 2px 5px;
        border-radius: 4px;
      }

      .product-detail {
        text-align: center;
        margin-top: 6px;
      }

      .product-title {
        display: block;
        color: #000;
        font-size: 12px;
        text-decoration: none;
        margin-bottom: 4px;
        line-height: 1.2;
      }

      .price-wrapper {
        font-size: 13px;
        font-weight: bold;
        color: #000;
      }

      @media (min-width: 768px) {
        #best-seller-popup {
          max-width: 500px;
          max-height: 500px;
        }

        .product-title {
          font-size: 13px;
        }

        .price-wrapper {
          font-size: 14px;
        }
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
      <h2>ÇOK SATANLAR</h2>
      ${state.products.map((p) => `
        <div class="product-best-wrapper">
          <div class="product-img">
            <a href="${p.url}">
              <img class="base-image" src="${p.image_url}" alt="${p.name}" />
              <img class="hover-image" src="${p.hover_image_url || p.image_url}" alt="${p.name}" />
            </a>
            <div class="hover-img-detail">
              <div class="product-code">${p.sku}</div>
            </div>
          </div>
          <div class="product-detail">
            <a href="${p.url}" class="product-title">${p.name}</a>
            <p class="price-wrapper">${parseFloat(p.price).toLocaleString("tr-TR")} TL</p>
          </div>
        </div>
      `).join("")}
    `;

    container.appendChild(css);
    container.appendChild(toggle);
    container.appendChild(popup);
    document.body.appendChild(container);
  }

  window.addEventListener("load", fetchProducts);
})();
