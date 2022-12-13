from pydantic import BaseModel


class BenchmarkNested(BaseModel):
    nested_name: str
    nested_number: int


class Benchmark(BaseModel):
    name: str
    number: int
    another_class: BenchmarkNested