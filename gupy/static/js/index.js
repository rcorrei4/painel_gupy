document.addEventListener('DOMContentLoaded', () => {
	steps()
})

function steps() {
	progressBars = document.querySelectorAll('.barra-progresso')

	progressBars.forEach((progressBar) => {
		width = (100/progressBar.dataset.etapas)*progressBar.dataset.etapa

		progressBar.style.width = `${width}%`
	})
}