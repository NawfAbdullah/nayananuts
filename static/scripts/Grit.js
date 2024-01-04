const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    async function waitForSelectors(selectors, frame) {
      for (const selector of selectors) {
        try {
          return await waitForSelector(selector, frame);
        } catch (err) {
          console.error(err);
        }
      }
      throw new Error('Could not find element for selectors: ' + JSON.stringify(selectors));
    }

    async function waitForSelector(selector, frame) {
      if (selector instanceof Array) {
        let element = null;
        for (const part of selector) {
          if (!element) {
            element = await frame.waitForSelector(part);
          } else {
            element = await element.$(part);
          }
          if (!element) {
            throw new Error('Could not find element: ' + part);
          }
          element = (await element.evaluateHandle(el => el.shadowRoot ? el.shadowRoot : el)).asElement();
        }
        if (!element) {
          throw new Error('Could not find element: ' + selector.join('|'));
        }
        return element;
      }
      const element = await frame.waitForSelector(selector);
      if (!element) {
        throw new Error('Could not find element: ' + selector);
      }
      return element;
    }

    async function waitForElement(step, frame) {
      const count = step.count || 1;
      const operator = step.operator || '>=';
      const comp = {
        '==': (a, b) => a === b,
        '>=': (a, b) => a >= b,
        '<=': (a, b) => a <= b,
      };
      const compFn = comp[operator];
      await waitForFunction(async () => {
        const elements = await querySelectorsAll(step.selectors, frame);
        return compFn(elements.length, count);
      });
    }

    async function querySelectorsAll(selectors, frame) {
      for (const selector of selectors) {
        const result = await querySelectorAll(selector, frame);
        if (result.length) {
          return result;
        }
      }
      return [];
    }

    async function querySelectorAll(selector, frame) {
      if (selector instanceof Array) {
        let elements = [];
        let i = 0;
        for (const part of selector) {
          if (i === 0) {
            elements = await frame.$$(part);
          } else {
            const tmpElements = elements;
            elements = [];
            for (const el of tmpElements) {
              elements.push(...(await el.$$(part)));
            }
          }
          if (elements.length === 0) {
            return [];
          }
          const tmpElements = [];
          for (const el of elements) {
            const newEl = (await el.evaluateHandle(el => el.shadowRoot ? el.shadowRoot : el)).asElement();
            if (newEl) {
              tmpElements.push(newEl);
            }
          }
          elements = tmpElements;
          i++;
        }
        return elements;
      }
      const element = await frame.$$(selector);
      if (!element) {
        throw new Error('Could not find element: ' + selector);
      }
      return element;
    }

    async function waitForFunction(fn) {
      let isActive = true;
      setTimeout(() => {
        isActive = false;
      }, 7000);
      while (isActive) {
        const result = await fn();
        if (result) {
          return;
        }
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      throw new Error('Timed out');
    }
    {
        const targetPage = page;
        await targetPage.setViewport({"width":927,"height":789})
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        await targetPage.goto('http://127.0.0.1:7000/');
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 0)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Shop"],["#cover > div > div.btn-holder > a.btn.btn-outline-light.btn-lg"]], targetPage);
        await element.click({ offset: { x: 37.703125, y: 36} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 300)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["body > section > div > div > div:nth-child(3) > div > div.card-footer.p-4.pt-0.border-top-0.bg-transparent > div > a"]], targetPage);
        await element.click({ offset: { x: 54.734375, y: 15.171875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 303)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Add to cart"],["body > section > div > div > div:nth-child(2) > div.d-flex > form > button"]], targetPage);
        await element.click({ offset: { x: 75, y: 5.6875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["aria/Email"],["#email"]], targetPage);
        await element.click({ offset: { x: 304.96875, y: 25.796875} });
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["aria/Email"],["#email"]], targetPage);
        const type = await element.evaluate(el => el.type);
        if (["textarea","select-one","text","url","tel","search","password","number","email"].includes(type)) {
          await element.type('admin@email.com');
        } else {
          await element.focus();
          await element.evaluate((el, value) => {
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
          }, "admin@email.com");
        }
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["aria/Password"],["#password"]], targetPage);
        await element.click({ offset: { x: 317.96875, y: 1.796875} });
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["aria/Password"],["#password"]], targetPage);
        const type = await element.evaluate(el => el.type);
        if (["textarea","select-one","text","url","tel","search","password","number","email"].includes(type)) {
          await element.type('1234');
        } else {
          await element.focus();
          await element.evaluate((el, value) => {
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
          }, "1234");
        }
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/Let me in!"],["#submit"]], targetPage);
        await element.click({ offset: { x: 39.96875, y: 24.796875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["#cover > div"]], targetPage);
        await element.click({ offset: { x: 895, y: 506} });
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Shop"],["#cover > div > div.btn-holder > a.btn.btn-outline-light.btn-lg"]], targetPage);
        await element.click({ offset: { x: 49.703125, y: 30} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 300)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["body > section > div > div > div:nth-child(3) > div > div.card-footer.p-4.pt-0.border-top-0.bg-transparent > div > a"]], targetPage);
        await element.click({ offset: { x: 42.734375, y: 33.171875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 300)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Add to cart"],["body > section > div > div > div:nth-child(2) > div.d-flex > form > button"]], targetPage);
        await element.click({ offset: { x: 58, y: 13.6875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 300)
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["body > section > div > div > div:nth-child(2) > div > div.card-footer.p-4.pt-0.border-top-0.bg-transparent > div > a"]], targetPage);
        await element.click({ offset: { x: 70.71875, y: 25.171875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Add to cart"],["body > section > div > div > div:nth-child(2) > div.d-flex > form > button"]], targetPage);
        await element.click({ offset: { x: 85, y: 22.6875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Add to cart"],["body > section > div > div > div:nth-child(2) > div.d-flex > form > button"]], targetPage);
        await element.click({ offset: { x: 85, y: 22.6875} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/ Cart 3.0"],["#navbarSupportedContent > form > a"]], targetPage);
        await element.click({ offset: { x: 61.453125, y: 16} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["body > form > div > div:nth-child(1) > div > div.col-md-8 > div > div > div > span:nth-child(3) > button"]], targetPage);
        await element.click({ offset: { x: 26.296875, y: 19} });
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["body > form > div > div:nth-child(1) > div > div.col-md-8 > div > div > div > span:nth-child(3) > button"]], targetPage);
        await element.click({ offset: { x: 26.296875, y: 19} });
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["body > form > div > div:nth-child(2) > div > div.col-md-8 > div > div > div > span:nth-child(3) > button"]], targetPage);
        await element.click({ offset: { x: 34.296875, y: 18} });
    }
    {
        const targetPage = page;
        const element = await waitForSelectors([["body > form > div > div:nth-child(2) > div > div.col-md-8 > div > div > div > span:nth-child(3) > button"]], targetPage);
        await element.click({ offset: { x: 34.296875, y: 18} });
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/Update"],["body > form > button"]], targetPage);
        await element.click({ offset: { x: 21, y: 30} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/Buy"],["body > form > a"]], targetPage);
        await element.click({ offset: { x: 6.921875, y: 18} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await targetPage.evaluate((x, y) => { window.scroll(x, y); }, 0, 300)
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/Place Order"],["body > div.form > form > button"]], targetPage);
        await element.click({ offset: { x: 53.59375, y: 28.25} });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        promises.push(targetPage.waitForNavigation());
        const element = await waitForSelectors([["aria/Keep Shoping"],["#login > div > div > a"]], targetPage);
        await element.click({ offset: { x: 610.203125, y: 20.828125} });
        await Promise.all(promises);
    }

    await browser.close();
})();
