function typewriterWithCursor(text, typeSpeed = 150, blinkSpeed = 500) {
    let index = 0;
    let isBlinking = false;
    let blinkInterval;

    // Fixed: Changed 'def' to 'function'
    function startBlinkingCursor() {
        blinkInterval = setInterval(() => {
            if (isBlinking) {
                document.title = text + " |";
            } else {
                document.title = text + "  "; 
            }
            isBlinking = !isBlinking;
        }, blinkSpeed);
    }

    const typeInterval = setInterval(() => {
        if (index <= text.length) {
            document.title = text.substring(0, index) + " |";
            index++;
        } else {
            clearInterval(typeInterval);
            startBlinkingCursor();
        }
    }, typeSpeed);
}

// Example usage:
typewriterWithCursor("cry for everything", 150, 500);