program test
implicit none
character(100) :: line
real :: data
open(unit=1,file = 'testdata.t', status = 'old', action = 'read')
read(1,'(A)') line
read(1,*) data
close(1)

write(*,*) line
write(*,*) data
end program
