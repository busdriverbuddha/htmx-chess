let lastClickedSquareName = "";

function startMove() {
    lastClickedSquareName = "";
}

function resetGame() {
    lastClickedSquareName = "";
    htmx.trigger("#message-box", "reload-message-box");
}

async function squareClicked(clickedSquare) {
    const clickedSquareName = clickedSquare.id.slice(-2);
    if (!lastClickedSquareName) {
        lastClickedSquareName = clickedSquareName;
    } else {
        try {
            const response = await fetch("/move/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ uci: `${lastClickedSquareName}${clickedSquareName}` })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.accepted) {
                    htmx.trigger("#board", "reload-board");
                }
                lastClickedSquareName = "";
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        } finally {
            htmx.trigger("#message-box", "reload-message-box");
        }
    }
}