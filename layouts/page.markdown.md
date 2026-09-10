{{- .Title | replaceRE "\n" " " | printf "# %s" }}
{{ partial "llms/localized-markdown.html" . }}
