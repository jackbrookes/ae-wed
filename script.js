(() => {
  // Tuning controls for the procedural ink texture. Adjust these values to change
  // blotch size, texture balance, and how far characters scatter from the reveal front.
  const INK_NOISE = Object.freeze({
    hashX: 127.1,
    hashY: 311.7,
    hashSeed: 74.7,
    hashMultiplier: 43758.5453123,
    octaveOneScale: 2.3,
    octaveOneWeight: 0.58,
    octaveTwoScale: 5.1,
    octaveTwoWeight: 0.29,
    octaveThreeScale: 15.2,
    octaveThreeWeight: 0.13,
    sampleXScale: 4.2,
    sampleYScale: 3.5,
    elementSeedStep: 19,
    characterSeedStep: 0.013,
    verticalWeight: 0.82,
    verticalOffset: 0.08,
    thresholdNoiseSpread: 0.34,
    thresholdMin: 0.025,
    thresholdMax: 0.975,
  });

  const INK_REVEAL = Object.freeze({
    transitionBand: 0.36,
    maximumBlurPx: 5.5,
  });

  // Personal contact and banking details are stored as a reversed encoded payload,
  // then assembled in the browser. This discourages simple source-scraping bots;
  // it is intentionally not presented as strong encryption.
  const privatePayload = '==QfiADNxAyN4YDI2cDI3YjMrIiOikXYsB3cpRUZu9GawJCLiADNxcDO2YzN3YjMiojIl52boBnIsISQOF0VTR1TCJiOiknc05WdvNmIsICWHdlQOJVSGJiOiQnZpd3ciwiIyUDM5IDN0cjMyYjI6ICduV3bjNWYiwiIFxUQItUQNByROV0UJJUQIRlTgU0QJ5UVFJiOiUWbh5mIsIiQC5kRiojIr5WYiJye';
  const privateDetails = JSON.parse(atob([...privatePayload].reverse().join('')));
  const bankFields = ['bank', 'name', 'account', 'swift', 'country'];
  const bankSummary = bankFields
    .map((field) => `${field === 'swift' ? 'SWIFT' : field[0].toUpperCase() + field.slice(1)}: ${privateDetails[field]}`)
    .join('\n');

  bankFields.forEach((field) => {
    const target = document.querySelector(`[data-bank-field="${field}"]`);
    if (target) target.textContent = privateDetails[field];
  });

  const whatsappLink = document.querySelector('[data-whatsapp-link]');
  const whatsappLabel = document.querySelector('[data-whatsapp-label]');
  if (whatsappLink) {
    const message = "Hello Anthony and Eunice, I'd like to RSVP for your wedding celebrations.";
    whatsappLink.href = `https://wa.me/${privateDetails.phone}?text=${encodeURIComponent(message)}`;
    whatsappLink.setAttribute(
      'aria-label',
      `RSVP to Anthony and Eunice on WhatsApp at ${privateDetails.phoneDisplay}`,
    );
  }
  if (whatsappLabel) whatsappLabel.textContent = privateDetails.phoneDisplay;

  const copyPlainText = async (value) => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }

    const textarea = document.createElement('textarea');
    textarea.value = value;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.append(textarea);
    textarea.select();
    const copied = document.execCommand('copy');
    textarea.remove();
    if (!copied) throw new Error('Copy command was unavailable');
  };

  const copyBankButton = document.querySelector('[data-copy-bank]');
  const copyLabel = document.querySelector('[data-copy-label]');
  const copyStatus = document.querySelector('[data-copy-status]');
  if (copyBankButton) {
    copyBankButton.disabled = false;
    copyBankButton.addEventListener('click', async () => {
      copyBankButton.disabled = true;
      try {
        await copyPlainText(bankSummary);
        if (copyLabel) copyLabel.textContent = 'Copied';
        if (copyStatus) copyStatus.textContent = 'Bank details copied to your clipboard.';
      } catch {
        if (copyLabel) copyLabel.textContent = 'Copy bank details';
        if (copyStatus) copyStatus.textContent = 'Copy failed. Please select the details above.';
      } finally {
        copyBankButton.disabled = false;
        window.setTimeout(() => {
          if (copyLabel) copyLabel.textContent = 'Copy bank details';
          if (copyStatus) copyStatus.textContent = '';
        }, 3000);
      }
    });
  }

  const inkSelector = [
    '[data-ink]',
    '.section-label',
    '.events-intro > p:last-child',
    '.event__number',
    '.event h2',
    '.event__subtitle',
    '.event__details dt',
    '.event__details dd',
    '.map-card a',
    '.dress-code__intro',
    '.dress-code__item h3',
    '.dress-code__item p',
    '.gifting__message',
    '.gifting__note',
    '.bank-details dt',
    '.bank-details dd',
    '.rsvp__note',
    '.rsvp__button',
    '.closing__date',
    '.back-to-top',
  ].join(',');
  const inkElements = [...document.querySelectorAll(inkSelector)];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const introDuration = 2500;
  const minimumRevealDuration = 1200;
  const introStartedAt = performance.now();
  let introComplete = reducedMotion.matches;
  let frameRequested = false;

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const smoothstep = (value) => {
    const x = clamp(value);
    return x * x * (3 - 2 * x);
  };

  // A deterministic hash and interpolated value-noise field. This only runs at layout time.
  const hash = (x, y, seed) => {
    const value = Math.sin(
      x * INK_NOISE.hashX +
      y * INK_NOISE.hashY +
      seed * INK_NOISE.hashSeed,
    ) * INK_NOISE.hashMultiplier;
    return value - Math.floor(value);
  };

  const valueNoise = (x, y, seed) => {
    const x0 = Math.floor(x);
    const y0 = Math.floor(y);
    const tx = x - x0;
    const ty = y - y0;
    const ux = tx * tx * (3 - 2 * tx);
    const uy = ty * ty * (3 - 2 * ty);
    const a = hash(x0, y0, seed);
    const b = hash(x0 + 1, y0, seed);
    const c = hash(x0, y0 + 1, seed);
    const d = hash(x0 + 1, y0 + 1, seed);
    const top = a + (b - a) * ux;
    const bottom = c + (d - c) * ux;
    return top + (bottom - top) * uy;
  };

  const fractalNoise = (x, y, seed) =>
    valueNoise(x * INK_NOISE.octaveOneScale, y * INK_NOISE.octaveOneScale, seed) * INK_NOISE.octaveOneWeight +
    valueNoise(x * INK_NOISE.octaveTwoScale, y * INK_NOISE.octaveTwoScale, seed + 3) * INK_NOISE.octaveTwoWeight +
    valueNoise(x * INK_NOISE.octaveThreeScale, y * INK_NOISE.octaveThreeScale, seed + 7) * INK_NOISE.octaveThreeWeight;

  const eligibleTextNodes = (element) => {
    const nodes = [];
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) => {
        const excludedParent = node.parentElement?.closest('svg, [aria-hidden="true"]');
        if (excludedParent && excludedParent !== element) return NodeFilter.FILTER_REJECT;
        return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    });

    while (walker.nextNode()) nodes.push(walker.currentNode);
    return nodes;
  };

  const createSpace = () => {
    const spaceSpan = document.createElement('span');
    spaceSpan.className = 'ink-char ink-char--space';
    spaceSpan.setAttribute('aria-hidden', 'true');
    // A non-breaking space keeps the generated gap tied to the inherited font
    // metrics and letter-spacing instead of imposing a one-size-fits-all width.
    spaceSpan.textContent = '\u00a0';
    return [spaceSpan, document.createElement('wbr')];
  };

  const hasContentSibling = (node, direction) => {
    let sibling = node[direction];
    while (sibling?.nodeType === Node.TEXT_NODE && !sibling.nodeValue.trim()) {
      sibling = sibling[direction];
    }
    return Boolean(sibling);
  };

  const prepareText = (element, index) => {
    const textNodes = eligibleTextNodes(element);
    const label = textNodes.map((node) => node.nodeValue).join(' ').replace(/\s+/g, ' ').trim();
    element.classList.add('ink-reveal');
    element.setAttribute('aria-label', label);

    textNodes.forEach((textNode) => {
      const original = textNode.nodeValue;
      const words = original.trim().split(/\s+/);
      const fragment = document.createDocumentFragment();

      if (/^\s/.test(original) && hasContentSibling(textNode, 'previousSibling')) {
        fragment.append(...createSpace());
      }

      words.forEach((word, wordIndex) => {
        const wordSpan = document.createElement('span');
        wordSpan.className = 'ink-word';
        wordSpan.setAttribute('aria-hidden', 'true');

        [...word].forEach((character) => {
          const characterSpan = document.createElement('span');
          characterSpan.className = 'ink-char';
          characterSpan.textContent = character;
          characterSpan.dataset.seed = String(index + 1);
          wordSpan.append(characterSpan);
        });

        fragment.append(wordSpan);
        if (wordIndex < words.length - 1) fragment.append(...createSpace());
      });

      if (/\s$/.test(original) && hasContentSibling(textNode, 'nextSibling')) {
        fragment.append(...createSpace());
      }
      textNode.replaceWith(fragment);
    });

    element.classList.add('ink-ready');
  };

  const measureText = (element, elementIndex) => {
    const bounds = element.getBoundingClientRect();
    const spans = [...element.querySelectorAll('.ink-char')];
    const width = Math.max(bounds.width, 1);
    const height = Math.max(bounds.height, 1);

    spans.forEach((span, characterIndex) => {
      const characterBounds = span.getBoundingClientRect();
      const x = (characterBounds.left - bounds.left + characterBounds.width * 0.5) / width;
      const y = (characterBounds.top - bounds.top + characterBounds.height * 0.5) / height;
      const noise = fractalNoise(
        x * INK_NOISE.sampleXScale,
        y * INK_NOISE.sampleYScale,
        elementIndex * INK_NOISE.elementSeedStep + characterIndex * INK_NOISE.characterSeedStep,
      );
      const verticalFront = y * INK_NOISE.verticalWeight + INK_NOISE.verticalOffset;
      span._inkThreshold = clamp(
        verticalFront + (noise - 0.5) * INK_NOISE.thresholdNoiseSpread,
        INK_NOISE.thresholdMin,
        INK_NOISE.thresholdMax,
      );
    });
  };

  const scrollProgressFor = (element) => {
    const bounds = element.getBoundingClientRect();
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const start = viewportHeight * 0.94;
    const travel = viewportHeight * 0.2 + Math.min(bounds.height * 0.55, viewportHeight * 0.13);
    return clamp((start - bounds.top) / travel);
  };

  const timeLimitedProgress = (element, target, timestamp) => {
    if (element._inkProgress === undefined) {
      element._inkProgress = 0;
      element._inkTimestamp = timestamp;
    }

    const elapsed = Math.min(Math.max(timestamp - element._inkTimestamp, 0), 50);
    element._inkTimestamp = timestamp;

    if (target < element._inkProgress) {
      element._inkProgress = target;
    } else {
      const maximumAdvance = elapsed / minimumRevealDuration;
      element._inkProgress = Math.min(target, element._inkProgress + maximumAdvance);
    }

    return element._inkProgress;
  };

  const paintText = (element, progress) => {
    if (
      element._paintedInkProgress !== undefined &&
      Math.abs(element._paintedInkProgress - progress) < 0.001
    ) {
      return;
    }
    element._paintedInkProgress = progress;

    const transitionBand = INK_REVEAL.transitionBand;
    element.querySelectorAll('.ink-char').forEach((span) => {
      const localProgress = smoothstep((progress - span._inkThreshold + transitionBand) / transitionBand);
      span.style.opacity = String(localProgress);
      if (localProgress > 0.985) {
        span.style.filter = 'none';
        span.style.willChange = 'auto';
      } else {
        span.style.filter = `blur(${((1 - localProgress) * INK_REVEAL.maximumBlurPx).toFixed(2)}px)`;
        span.style.willChange = 'opacity, filter';
      }
    });
  };

  const updateInk = (timestamp = performance.now()) => {
    frameRequested = false;

    if (reducedMotion.matches) {
      inkElements.forEach((element) => {
        element._inkProgress = 1;
        element._inkTimestamp = timestamp;
        paintText(element, 1);
      });
      return;
    }

    const introProgress = clamp((timestamp - introStartedAt) / introDuration);
    const easedIntro = 1 - Math.pow(1 - introProgress, 3);
    let needsContinuation = false;

    inkElements.forEach((element) => {
      const scrollProgress = scrollProgressFor(element);
      const wasInitiallyVisible = element._initiallyVisible;
      const targetProgress = !introComplete && wasInitiallyVisible
        ? scrollProgress * easedIntro
        : scrollProgress;
      const progress = timeLimitedProgress(element, targetProgress, timestamp);
      paintText(element, progress);
      if (progress < targetProgress - 0.001) needsContinuation = true;
    });

    if (!introComplete && introProgress >= 1) introComplete = true;

    if (!introComplete || needsContinuation) {
      frameRequested = true;
      requestAnimationFrame(updateInk);
    }
  };

  const requestUpdate = () => {
    if (!frameRequested) {
      frameRequested = true;
      requestAnimationFrame(updateInk);
    }
  };

  const measureAll = () => {
    inkElements.forEach((element, index) => {
      measureText(element, index);
      element._paintedInkProgress = undefined;
    });
    requestUpdate();
  };

  inkElements.forEach(prepareText);
  inkElements.forEach((element) => {
    const bounds = element.getBoundingClientRect();
    element._initiallyVisible = bounds.top < window.innerHeight && bounds.bottom > 0;
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('is-visible');
      });
    },
    { rootMargin: '0px 0px -10% 0px', threshold: 0.12 },
  );
  document.querySelectorAll('.reveal-on-scroll').forEach((element) => observer.observe(element));

  measureAll();
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', measureAll, { passive: true });
  reducedMotion.addEventListener?.('change', requestUpdate);
  document.fonts?.ready.then(measureAll);
})();
