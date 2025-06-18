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
        border: 1px solid #ebbecb;
        box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        overflow-y: auto;
        z-index: 9999;
        display: none;
      }
      .product-best-wrapper {
        width: 50%;
        float: left;
        box-sizing: border-box;
        padding: 10px;
        border: 1px solid #ebbecb;
      }
      .product-img {
        position: relative;
      }
      .base-image, .hover-image {
        width: 100%;
        height: auto;
        display: block;
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
        bottom: 10px;
        left: 10px;
        color: white;
        font-size: 12px;
      }
      .product-code {
        background: rgba(0,0,0,0.6);
        padding: 2px 6px;
        border-radius: 4px;
      }
      .product-detail {
        text-align: center;
        margin-top: 10px;
      }
      .product-title {
        display: block;
        color: #000;
        font-size: 14px;
        text-decoration: none;
        margin-bottom: 4px;
      }
      .price-wrapper {
        font-size: 16px;
        font-weight: bold;
        color: #000;
      }
    `;

    const css = document.createElement("style");
    css.innerText = style;

    const toggle = document.createElement("div");
    toggle.id = "best-seller-toggle";
    toggle.innerText = "💎";
    toggle.onclick = () => {
      state.visible = !state.visible;
      document.getElementById("best-seller-popup").style.display = state.visible ? "block" : "none";
    };

    const popup = document.createElement("div");
    popup.id = "best-seller-popup";
    popup.innerHTML = `
      <h2 style="text-align:center; font-weight:bold; margin-bottom:20px;">ÇOK SATANLAR</h2>
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
        </div>`).join("")}
    `;

    container.appendChild(css);
    container.appendChild(toggle);
    container.appendChild(popup);
    document.body.appendChild(container);
  }

  window.addEventListener("load", fetchProducts);
})();
