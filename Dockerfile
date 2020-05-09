FROM python:3

WORKDIR usr/src/sudoku-solver

COPY ./ ./

CMD ["python", "sudoku-solver.py"]