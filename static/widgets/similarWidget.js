(function () {
  console.log("🧪 Worker etiketi başarıyla yüklendi!");

  const { sku, price } = getSKUAndPrice();
  const userId = getUserId();

  if (sku) {
    sendEvent("view_item", {
      product_id: sku,
      event_value: price ? String(price) : null
    });

    // ✅ Benzer ürün widget'ı başlatılsın
    console.log("👀 Benzer ürün widget başlatıldı: Ürün ID =", sku);

    fetch(`https://searchprojectdemo.com/api/recommendations/similar/${sku}`)
      .then(res => res.json())
      .then(data => {
        const verticalTab = document.querySelector(".vertical-tab");
        if (!verticalTab) return console.warn("❌ .vertical-tab bulunamadı");

        // Eğer widget daha önce eklenmişse tekrar ekleme
        if (document.querySelector("#similar-products-widget")) return;

        const container = document.createElement("div");
        container.id = "similar-products-widget";
        container.style.padding = "20px 0";

        // Ürünleri HTML olarak ekle
        if (data.products?.length) {
          data.products.forEach(p => {
            const item = document.createElement("div");
            item.style.marginBottom = "15px";
            item.innerHTML = `
              <a href="${p.url}" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
                <img src="${p.image}" style="width: 80px; height: auto; margin-right: 10px;" />
                <div>
                  <div><strong>${p.name}</strong></div>
                  <div>${p.price} TL</div>
                </div>
              </a>
            `;
            container.appendChild(item);
          });
        } else {
          container.innerHTML = "<p>Benzer ürün bulunamadı.</p>";
        }

        // vertical-tab'den sonra ekle
        verticalTab.parentNode.insertBefore(container, verticalTab.nextSibling);
      });
  }

  function getUserId() {
    let userId = localStorage.getItem("user_id");
    if (!userId) {
      userId = "user-" + Math.random().toString(36).substring(2);
      localStorage.setItem("user_id", userId);
    }
    return userId;
  }

  function getSKUAndPrice() {
    let sku = null;
    let price = null;

    try {
      const script = document.querySelector('script[type="application/ld+json"]');
      const json = JSON.parse(script?.innerText || "{}");

      if (json["@graph"] && Array.isArray(json["@graph"])) {
        const graphItem = json["@graph"].find(item => item.sku);
        sku = graphItem?.sku || null;
        price = graphItem?.offers?.price || null;
      }
    } catch (e) {
      console.warn("⚠️ JSON-LD parse edilemedi:", e);
    }

    if (!price) {
      const priceEl = document.querySelector("p.product-info-price");
      if (priceEl) {
        price = priceEl.innerText.replace(/[^0-9]/g, "");
      }
    }

    return { sku, price };
  }

  function sendEvent(eventName, extraData = {}) {
    const data = {
      event_name: eventName,
      user_id: userId,
      ...extraData,
      utm_source: localStorage.getItem("utm_source") || null
    };

    fetch("https://searchprojectdemo.com/api/track-event/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    }).then(() => {
      console.log("📡 Event gönderildi:", eventName, data);
    });
  }
})();
