# Defense package — build note

`defense/*.md` are the canonical defense content sources. The D5.14
package spec names PDF exports (`architecture.pdf`, `equations.pdf`,
`experiment_matrix.pdf`, `result_provenance.pdf`, `bdhr_bdchq_notes.pdf`
plus `anticipated_questions.md`).

No PDF toolchain is present in this development environment
(no pandoc/wkhtmltopdf/LaTeX). At packaging time, on the release
machine:

```bash
pip install markdown      # or use pandoc if available
pandoc defense/architecture.md -o defense/architecture.pdf
pandoc defense/equations.md -o defense/equations.pdf
pandoc defense/experiment_matrix.md -o defense/experiment_matrix.pdf
pandoc defense/result_provenance.md -o defense/result_provenance.pdf
pandoc defense/bdhr_bdchq_notes.md -o defense/bdhr_bdchq_notes.pdf
# anticipated_questions.md is kept as markdown (already human-readable)
```

`sources.md` confirm: all content is ours; no paper figures or text are
redistributed in these exports.